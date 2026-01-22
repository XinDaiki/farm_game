import pygame
import sys
import json
from settings import *
from player import Player
from inventory import Inventory
from crafting import Crafting
from world import World
from animal import Animal
from npc import NPC
from time_system import TimeSystem
from ui import UI
from plot_system import PlotSystem
from quest_system import QuestSystem

class FarmGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), 
                                              pygame.RESIZABLE)
        pygame.display.set_caption("Pixel Farm - Harvest Valley")
        self.clock = pygame.time.Clock()
        
        # Track current window size
        self.screen_width = DEFAULT_SCREEN_WIDTH
        self.screen_height = DEFAULT_SCREEN_HEIGHT
        
        # Create world surface (fixed size for game world)
        self.world_width = TILE_SIZE * MAP_WIDTH
        self.world_height = TILE_SIZE * MAP_HEIGHT
        self.world_surface = pygame.Surface((self.world_width, self.world_height))
        
        # Game objects
        self.player = Player((self.world_width // 2, self.world_height // 2))
        self.world = World()
        self.world.create_default_map()
        
        # Animals - NOW WITH MORE VARIETY!
        self.animals = pygame.sprite.Group()
        # Original animals
        self.animals.add(Animal((300, 300), "chicken"))
        self.animals.add(Animal((350, 320), "chicken"))
        self.animals.add(Animal((500, 400), "cow"))
        
        # New animals
        self.animals.add(Animal((400, 350), "pig"))
        self.animals.add(Animal((550, 320), "rabbit"))
        self.animals.add(Animal((380, 280), "turkey"))
        
        # NPCs
        self.npcs = pygame.sprite.Group()
        self.shopkeeper = NPC((100, 150), "shopkeeper")
        self.mayor = NPC((self.world_width - 100, 150), "mayor")
        self.npcs.add(self.shopkeeper, self.mayor)
        
        # Show welcome message
        self.show_notification("Welcome! Press F near Shopkeeper to trade!")
        self.notification_timer = 300
        
        # Systems
        self.inventory = Inventory()
        self.crafting = Crafting()
        self.time_system = TimeSystem()
        self.ui = UI()
        self.plot_system = PlotSystem()
        self.quest_system = QuestSystem()
        
        # Track last completed quest for notification
        self.last_completed_quest = None
        self.quest_notification_timer = 0
        
        # Game state
        self.show_grid = False
        self.notification = ""
        self.notification_timer = 0
        self.paused = False
        self.show_exit_confirmation = False
        
        # Interaction
        self.nearby_npc = None
        self.nearby_animal = None
        self.interaction_distance = 60
        
        # Interaction prompt animation
        self.prompt_timer = 0
        self.prompt_fade_duration = 120  # 2 seconds at 60 FPS to fully fade
        self.prompt_shown = False  # Track if prompt was already shown

        self.font = pygame.font.SysFont(Arial, 18)
        
        # Settings button rect
        self.settings_button_rect = None
        
    def handle_resize(self, width, height):
        """Handle window resize event"""
        self.screen_width = max(MIN_SCREEN_WIDTH, width)
        self.screen_height = max(MIN_SCREEN_HEIGHT, height)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                              pygame.RESIZABLE)
        # Update global settings
        update_screen_size(self.screen_width, self.screen_height)
        
    def screen_to_world_pos(self, screen_pos):
        """Convert screen position to world position"""
        # Calculate scale to fit world in window
        scale_x = self.screen_width / self.world_width
        scale_y = self.screen_height / self.world_height
        scale = min(scale_x, scale_y)
        
        # Calculate scaled dimensions and offset
        scaled_width = int(self.world_width * scale)
        scaled_height = int(self.world_height * scale)
        offset_x = (self.screen_width - scaled_width) // 2
        offset_y = (self.screen_height - scaled_height) // 2
        
        # Adjust for world offset
        adjusted_x = screen_pos[0] - offset_x
        adjusted_y = screen_pos[1] - offset_y
        
        # Scale to world coordinates
        world_x = adjusted_x / scale
        world_y = adjusted_y / scale
        
        return (int(world_x), int(world_y))
    
    def is_click_in_world(self, screen_pos):
        """Check if a screen position is within the world area"""
        scale_x = self.screen_width / self.world_width
        scale_y = self.screen_height / self.world_height
        scale = min(scale_x, scale_y)
        
        scaled_width = int(self.world_width * scale)
        scaled_height = int(self.world_height * scale)
        offset_x = (self.screen_width - scaled_width) // 2
        offset_y = (self.screen_height - scaled_height) // 2
        
        x, y = screen_pos
        return (offset_x <= x < offset_x + scaled_width and
                offset_y <= y < offset_y + scaled_height)
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
                
            elif event.type == pygame.MOUSEWHEEL:
                # Handle scrolling in controls panel
                if self.ui.handle_scroll(event, self.screen_width, self.screen_height):
                    continue
                
            elif event.type == pygame.KEYDOWN:
                # F key - Interact with nearby NPCs/Animals
                if event.key == pygame.K_f:
                    if self.nearby_npc:
                        self.interact_with_npc(self.nearby_npc)
                    elif self.nearby_animal:
                        self.interact_with_animal(self.nearby_animal)
                
                # L key - Toggle plot lock at mouse position
                elif event.key == pygame.K_l:
                    screen_pos = pygame.mouse.get_pos()
                    if self.is_click_in_world(screen_pos):
                        world_pos = self.screen_to_world_pos(screen_pos)
                        grid_x = world_pos[0] // TILE_SIZE
                        grid_y = world_pos[1] // TILE_SIZE
                        grid_pos = (grid_x, grid_y)
                        
                        if self.plot_system.is_claimed(grid_pos):
                            success, message = self.plot_system.toggle_lock(grid_pos)
                            if message:
                                self.show_notification(message)
                
                # Tool selection
                elif event.key == pygame.K_t:
                    self.player.change_tool()
                    self.show_notification(f"Tool: {self.player.current_tool.replace('_', ' ').title()}")
                    
                # Hotbar selection (1-5)
                elif event.key == pygame.K_1:
                    self.inventory.selected_hotbar_slot = 0
                elif event.key == pygame.K_2:
                    self.inventory.selected_hotbar_slot = 1
                elif event.key == pygame.K_3:
                    self.inventory.selected_hotbar_slot = 2
                elif event.key == pygame.K_4:
                    self.inventory.selected_hotbar_slot = 3
                elif event.key == pygame.K_5:
                    self.inventory.selected_hotbar_slot = 4
                    
                # Toggle systems
                elif event.key == pygame.K_e:
                    self.inventory.toggle_inventory()
                elif event.key == pygame.K_c: 
                    #self.show_notification("Crafting menu is currently disabled.")
                    self.crafting.toggle_menu()
                elif event.key == pygame.K_q:
                    self.quest_system.toggle_quest_tab()
                elif event.key == pygame.K_i:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_h:
                    self.show_notification("Shopkeeper is in top-left area with 'SHOP' label!")
                    
                # Close shop with ESC or show exit confirmation
                elif event.key == pygame.K_ESCAPE:
                    if self.shopkeeper.shop_mode:
                        self.shopkeeper.shop_mode = None
                    elif self.show_exit_confirmation:
                        # Close the exit dialog if ESC is pressed again
                        self.show_exit_confirmation = False
                    else:
                        # Show exit confirmation dialog
                        self.show_exit_confirmation = True
                
                # Handle exit confirmation
                elif event.key == pygame.K_y and self.show_exit_confirmation:
                    self.save_game()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n and self.show_exit_confirmation:
                    self.show_exit_confirmation = False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check settings button click
                if self.settings_button_rect and self.settings_button_rect.collidepoint(mouse_pos) and event.button == 1:
                    self.ui.toggle_controls()
                    continue
                
                # Handle inventory clicks first
                if self.inventory.show_full_inventory and event.button == 1:
                    if self.inventory.handle_inventory_click(mouse_pos, self.screen_width, self.screen_height):
                        continue
                
                # Handle quest tab clicks
                if self.quest_system.show_quest_tab and event.button == 1:
                    result = self.quest_system.handle_click(mouse_pos, self.screen_width, 
                                                           self.screen_height, self.player, self.inventory)
                    if result:
                        self.show_notification(result)
                        continue
                
                # Don't process tool/interact clicks if inventory or quest tab is open
                if self.inventory.show_full_inventory or self.quest_system.show_quest_tab:
                    continue
                
                # Handle crafting menu clicks
                if self.crafting.show_menu and event.button == 1:
                    if self.crafting.handle_click(mouse_pos, self.inventory, self.screen_width, self.screen_height):
                        self.show_notification("Item crafted!")
                        
                        # Track crafted item for quests
                        for recipe_name in self.crafting.recipes:
                            completed = self.quest_system.update_quest("craft", recipe_name, 1)
                            if completed:
                                self.last_completed_quest = completed
                                self.quest_notification_timer = 180
                            break
                        
                # Handle shop clicks
                elif self.shopkeeper.shop_mode and event.button == 1:
                    action, result, message = self.shopkeeper.handle_shop_click(
                        mouse_pos, self.player, self.inventory, self.screen_width, self.screen_height
                    )
                    if message:
                        self.show_notification(message)
                    
                # Left click - use tool (only if clicking in world area)
                elif event.button == 1 and not self.crafting.show_menu:
                    if self.is_click_in_world(mouse_pos):
                       world_pos = self.screen_to_world_pos(mouse_pos)
                       self.use_tool(world_pos)
                    
                # Right click - claim or sell plots
                elif event.button == 3:
                    if self.shopkeeper.shop_mode:
                        self.shopkeeper.shop_mode = None
                    elif self.is_click_in_world(mouse_pos):
                        world_pos = self.screen_to_world_pos(mouse_pos)
                        grid_x = world_pos[0] // TILE_SIZE
                        grid_y = world_pos[1] // TILE_SIZE
                        grid_pos = (grid_x, grid_y)
                        
                        # Check if plot is already claimed - if so, try to sell
                        if self.plot_system.is_claimed(grid_pos):
                            success, message = self.plot_system.sell_plot(grid_pos, self.player, self.world)
                            if message:
                                self.show_notification(message)
                        else:
                            # Try to claim plot
                            success, message = self.plot_system.claim_plot(grid_pos, self.player, self.world)
                            if success or message:
                                self.show_notification(message)
                                
                                if success:
                                    # Update quest
                                    completed = self.quest_system.update_quest("claim", "plot", 1)
                                    if completed:
                                        self.last_completed_quest = completed
                                        self.quest_notification_timer = 180
    
    def check_nearby_entities(self):
        """Check for nearby NPCs and animals for F key interaction"""
        player_pos = pygame.math.Vector2(self.player.rect.center)
        
        # Check NPCs
        self.nearby_npc = None
        for npc in self.npcs:
            npc_pos = pygame.math.Vector2(npc.rect.center)
            distance = player_pos.distance_to(npc_pos)
            if distance <= self.interaction_distance:
                self.nearby_npc = npc
                break
        
        # Check animals (only if no NPC nearby)
        self.nearby_animal = None
        if not self.nearby_npc:
            for animal in self.animals:
                animal_pos = pygame.math.Vector2(animal.rect.center)
                distance = player_pos.distance_to(animal_pos)
                if distance <= self.interaction_distance:
                    self.nearby_animal = animal
                    break
    
    def interact_with_npc(self, npc):
        """Interact with an NPC"""
        dialogue = npc.talk()
    
    def interact_with_animal(self, animal):
        """Interact with an animal"""
        # Check animal state and respond accordingly
        if animal.can_collect():
            # Collect product
            product, value = animal.collect_product()
            if product:
                self.inventory.add_item(product, 1)
                self.show_notification(f"Collected {product.replace('_', ' ')}! You can now feed the animal again!")
                
                # Update quests
                completed = self.quest_system.update_quest("collect", product, 1)
                if completed:
                    self.last_completed_quest = completed
                    self.quest_notification_timer = 180
                    
        elif animal.can_feed():
            # Feed the animal
            if animal.feed():
                self.show_notification(f"Fed {animal.animal_type}! Wait for digestion.")
                
                # Update quests
                completed = self.quest_system.update_quest("feed", "animal", 1)
                if completed:
                    self.last_completed_quest = completed
                    self.quest_notification_timer = 180
        else:
            # Animal is in cooldown or producing
            state_info = animal.get_state_info()
            self.show_notification(f"{animal.animal_type.title()}: {state_info}")
                        
    def use_tool(self, pos):
        """Use the currently equipped tool"""
        tool = self.player.current_tool
        
        if tool == "hoe":
            # Till soil - ONLY on claimed plots
            grid_x = pos[0] // TILE_SIZE
            grid_y = pos[1] // TILE_SIZE
            grid_pos = (grid_x, grid_y)
            
            if not self.plot_system.is_claimed(grid_pos):
                self.show_notification("Must claim plot first! (Right-click grass)")
                return
            
            if self.player.use_energy(5):
                if self.world.till(pos):
                    self.show_notification("Soil tilled!")
                    
                    # Update quests
                    completed = self.quest_system.update_quest("till", "soil", 1)
                    if completed:
                        self.last_completed_quest = completed
                        self.quest_notification_timer = 180
                    
        elif tool == "watering_can":
            # Water crops and soil
            if self.player.use_energy(3):
                if self.world.water(pos):
                    self.show_notification("Watered!")
                    
                    # Update quests
                    completed = self.quest_system.update_quest("water", "crop", 1)
                    if completed:
                        self.last_completed_quest = completed
                        self.quest_notification_timer = 180
                    
        elif tool == "hand":
            # Plant or harvest
            crop_type = self.inventory.get_selected_seed()
            if crop_type:
                seed_name = f"{crop_type}_seed"
                if self.inventory.use(seed_name):
                    if self.world.plant(pos, crop_type):
                        self.show_notification(f"Planted {crop_type}!")
                        
                        # Update quests
                        completed = self.quest_system.update_quest("plant", crop_type, 1)
                        if completed:
                            self.last_completed_quest = completed
                            self.quest_notification_timer = 180
                    else:
                        # Refund seed if planting failed
                        self.inventory.add_item(seed_name, 1)
            else:
                # Try to harvest
                crop_type, value = self.world.harvest(pos)
                if crop_type:
                    self.inventory.add_item(crop_type, 1)
                    self.show_notification(f"Harvested {crop_type}! Sell to shopkeeper!")
                    
                    # Update quests
                    completed = self.quest_system.update_quest("harvest", crop_type, 1)
                    if completed:
                        self.last_completed_quest = completed
                        self.quest_notification_timer = 180
                    
        elif tool == "axe":
            # Chop trees for wood
            tile = self.world.get_tile_at_pos(pos)
            if tile and tile.kind == "T" and self.player.use_energy(10):
                self.inventory.add_item("wood", 3)
                self.show_notification("Chopped wood! +3 wood")
                
                # Update quests
                completed = self.quest_system.update_quest("collect", "wood", 3)
                if completed:
                    self.last_completed_quest = completed
                    self.quest_notification_timer = 180
                
        elif tool == "scythe":
            # Clear grass
            tile = self.world.get_tile_at_pos(pos)
            if tile and tile.kind == "G" and self.player.use_energy(2):
                self.show_notification("Cleared grass!")
                
    def show_notification(self, message):
        """Show a notification message"""
        self.notification = message
        self.notification_timer = 120
        
    def update(self, dt):
        """Update all game systems"""
        if self.paused:
            return
            
        keys = pygame.key.get_pressed()
        
        # Update systems
        self.player.update(keys, dt)
        self.world.update()
        self.time_system.update(dt)
        
        # Check for nearby entities
        self.check_nearby_entities()
        
        # Update animals
        for animal in self.animals:
            animal.update(dt)
            
        # Update NPCs
        for npc in self.npcs:
            npc.update(dt)
            
        # Update notification
        if self.notification_timer > 0:
            self.notification_timer -= 1
            if self.notification_timer == 0:
                self.notification = ""
        
        # Update quest notification
        if self.quest_notification_timer > 0:
            self.quest_notification_timer -= 1
            if self.quest_notification_timer == 0:
                self.last_completed_quest = None
        
        # Update interaction prompt animation timer
        if self.nearby_npc or self.nearby_animal:
            if self.prompt_timer < self.prompt_fade_duration:
                self.prompt_timer += 1
        else:
            # Reset when leaving the area
            self.prompt_timer = 0
        
        # Update quest for money (check periodically)
        if hasattr(self, 'last_money_check'):
            if self.player.money != self.last_money_check:
                self.quest_system.update_quest("money", "total", self.player.money)
                self.last_money_check = self.player.money
        else:
            self.last_money_check = self.player.money
                
    def draw(self):
        """Draw everything"""
        # Clear screen with black
        self.screen.fill(BLACK)
        
        # Draw world to world surface
        self.world_surface.fill(BLACK)
        self.world.tiles.draw(self.world_surface)
        
        # Draw claimed plot indicators
        self.plot_system.draw_claimed_indicators(self.world_surface)
        
        # Draw grid if enabled
        if self.show_grid:
            self.world.draw_grid(self.world_surface)
            
        # Draw crops
        self.world.crops.draw(self.world_surface)
        
        # Draw crop status indicators
        for crop in self.world.crops:
            crop.draw_status(self.world_surface)
        
        # Draw animals
        self.animals.draw(self.world_surface)
        for animal in self.animals:
            animal.draw_status(self.world_surface)
            
        # Draw NPCs
        self.npcs.draw(self.world_surface)
        for npc in self.npcs:
            npc.draw_label(self.world_surface)
            npc.draw_dialogue(self.world_surface)
            
        # Draw player
        self.world_surface.blit(self.player.image, self.player.rect)
        
        # Draw interaction prompt (in world space)
        if self.nearby_npc:
            self.draw_interaction_prompt_world(self.world_surface, 
                                              self.nearby_npc.rect.centerx, 
                                              self.nearby_npc.rect.top - 30, 
                                              f"Press [F] to talk to {self.nearby_npc.npc_type.title()}")
        elif self.nearby_animal:
            if self.nearby_animal.can_collect():
                action = "Collect"
            elif self.nearby_animal.can_feed():
                action = "Feed"
            else:
                action = "Check"
            self.draw_interaction_prompt_world(self.world_surface,
                                              self.nearby_animal.rect.centerx, 
                                              self.nearby_animal.rect.top - 30,
                                              f"Press [F] to {action} {self.nearby_animal.animal_type.title()}")
        
        # Draw claimable/sellable plot hint (only if inventory not open) - in world space
        if not self.inventory.show_full_inventory:
            screen_mouse_pos = pygame.mouse.get_pos()
            if self.is_click_in_world(screen_mouse_pos):
                world_mouse_pos = self.screen_to_world_pos(screen_mouse_pos)
                self.plot_system.draw_claimable_hint(self.world_surface, world_mouse_pos, self.world, self.player)
        
        # Apply darkness for night
        if self.time_system.is_night():
            darkness = pygame.Surface((self.world_width, self.world_height))
            darkness.set_alpha(self.time_system.get_darkness_alpha())
            darkness.fill((0, 0, 40))
            self.world_surface.blit(darkness, (0, 0))
        
        # Scale world to fill window while maintaining aspect ratio
        scale_x = self.screen_width / self.world_width
        scale_y = self.screen_height / self.world_height
        scale = min(scale_x, scale_y)
        
        scaled_width = int(self.world_width * scale)
        scaled_height = int(self.world_height * scale)
        offset_x = (self.screen_width - scaled_width) // 2
        offset_y = (self.screen_height - scaled_height) // 2
        
        scaled_surface = pygame.transform.scale(self.world_surface, (scaled_width, scaled_height))
        self.screen.blit(scaled_surface, (offset_x, offset_y))
        
        # Draw UI elements (screen space)
        self.ui.draw_player_stats(self.screen, self.player, self.time_system)
        self.ui.draw_controls(self.screen, self.screen_width, self.screen_height)
        
        # Draw inventory (hotbar always visible, full inventory when toggled)
        self.inventory.draw(self.screen, self.screen_width, self.screen_height)
        
        # Draw crafting menu
        self.crafting.draw_menu(self.screen, self.inventory, self.screen_width, self.screen_height)
        
        # Draw quest tab
        self.quest_system.draw_quest_tab(self.screen, self.screen_width, self.screen_height)
        
        # Draw quest notification
        if self.last_completed_quest and self.quest_notification_timer > 0:
            self.quest_system.draw_quest_notification(self.last_completed_quest, 
                                                     self.screen, self.screen_width, self.screen_height)
        
        # Draw shop menus
        if self.shopkeeper.shop_mode:
            self.shopkeeper.draw_shop_menu(self.screen, self.screen_width, self.screen_height)
            self.shopkeeper.draw_buy_menu(self.screen, self.player.money, self.screen_width, self.screen_height)
            self.shopkeeper.draw_sell_menu(self.screen, self.inventory, self.player.money, self.screen_width, self.screen_height)
                
        # Draw notification
        if self.notification:
            self.ui.draw_notification(self.screen, self.notification, self.screen_width, self.screen_height)
        
        # Draw settings button (always on top)
        self.settings_button_rect = self.ui.draw_settings_button(self.screen, self.screen_width, self.screen_height)
        
        # Draw exit confirmation dialog (if active)
        if self.show_exit_confirmation:
            self.draw_exit_confirmation()
            
        # Update display
        pygame.display.flip()
    
    def draw_interaction_prompt_world(self, surface, x, y, text):
        """Draw interaction prompt in world space with fade-out animation"""
        # Calculate alpha based on timer - fade from 255 to 0 over 2 seconds
        fade_progress = self.prompt_timer / self.prompt_fade_duration
        alpha = int(255 * (1 - fade_progress))
        
        # Don't draw if fully faded
        if alpha <= 0:
            return

        prompt_font = pygame.font.SysFont(Arial, 12)
        text_surface = prompt_font.render(text, True, WHITE)
        
        # Background
        padding = 6
        bg_width = text_surface.get_width() + padding * 2
        bg_height = text_surface.get_height() + padding * 2
        bg_x = x - bg_width // 2
        bg_y = y
        
        bg = pygame.Surface((bg_width, bg_height))
        bg.set_alpha(int(220 * (alpha / 255)))  # Scale background alpha
        bg.fill((40, 40, 40))
        surface.blit(bg, (bg_x, bg_y))
        
        # Border - create a surface with alpha
        border_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, (*YELLOW, alpha), (0, 0, bg_width, bg_height), 2)
        surface.blit(border_surface, (bg_x, bg_y))
        
        # Text with alpha
        text_with_alpha = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
        text_with_alpha.fill((0, 0, 0, 0))
        temp_text = prompt_font.render(text, True, (*WHITE, alpha))
        text_with_alpha.blit(temp_text, (0, 0))
        text_with_alpha.set_alpha(alpha)
        
        text_x = bg_x + padding
        text_y = bg_y + padding
        surface.blit(text_with_alpha, (text_x, text_y))
    
    def draw_exit_confirmation(self):
        """Draw exit confirmation dialog"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 400
        dialog_height = 150
        dialog_x = (self.screen_width - dialog_width) // 2
        dialog_y = (self.screen_height - dialog_height) // 2
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Title text
        title_font = pygame.font.SysFont(Arial, 28)
        title_text = title_font.render("Exit Game?", True, WHITE)
        title_x = dialog_x + (dialog_width - title_text.get_width()) // 2
        title_y = dialog_y + 20
        self.screen.blit(title_text, (title_x, title_y))
        
        # Message text
        message_font = pygame.font.SysFont(Arial, 18)
        message_text = message_font.render("Do you want to exit the game?", True, WHITE)
        message_x = dialog_x + (dialog_width - message_text.get_width()) // 2
        message_y = dialog_y + 60
        self.screen.blit(message_text, (message_x, message_y))
        
        # Instructions
        instruction_font = pygame.font.SysFont(Arial, 16)
        yes_text = instruction_font.render("Press [Y] for Yes", True, (100, 255, 100))
        no_text = instruction_font.render("Press [N] for No", True, (255, 100, 100))
        
        yes_x = dialog_x + dialog_width // 4 - yes_text.get_width() // 2
        no_x = dialog_x + 3 * dialog_width // 4 - no_text.get_width() // 2
        instruction_y = dialog_y + 100
        
        self.screen.blit(yes_text, (yes_x, instruction_y))
        self.screen.blit(no_text, (no_x, instruction_y))
        
    def save_game(self):
        """Save game state"""
        save_data = {
            "player": {
                "pos": self.player.rect.center,
                "money": self.player.money,
                "energy": self.player.energy
            },
            "inventory": self.inventory.items,
            "hotbar": self.inventory.hotbar,
            "time": {
                "time": self.time_system.time,
                "day": self.time_system.day,
                "season": self.time_system.season
            },
            "plots": self.plot_system.save_data(),
            "quests": self.quest_system.save_data()
        }
        
        try:
            with open("save_game.json", "w") as f:
                json.dump(save_data, f, indent=2)
            print("Game saved!")
        except Exception as e:
            print(f"Error saving game: {e}")
            
    def load_game(self):
        """Load game state"""
        try:
            with open("save_game.json", "r") as f:
                save_data = json.load(f)
                
            # Restore player
            self.player.rect.center = tuple(save_data["player"]["pos"])
            self.player.money = save_data["player"]["money"]
            self.player.energy = save_data["player"]["energy"]
            
            # Restore inventory
            self.inventory.items = save_data["inventory"]
            
            # Restore hotbar
            if "hotbar" in save_data:
                self.inventory.hotbar = save_data["hotbar"]
            
            # Restore time
            self.time_system.time = save_data["time"]["time"]
            self.time_system.day = save_data["time"]["day"]
            self.time_system.season = save_data["time"]["season"]
            
            # Restore plots
            if "plots" in save_data:
                self.plot_system.load_data(save_data["plots"])
            
            # Restore quests
            if "quests" in save_data:
                self.quest_system.load_data(save_data["quests"])
            
            print("Game loaded!")
            return True
        except FileNotFoundError:
            print("No save file found, starting new game")
            return False
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
            
    def run(self):
        """Main game loop"""
        # Try to load save
        self.load_game()
        
        while True:
            dt = self.clock.tick(FPS) / 16.67
            
            self.handle_events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    game = FarmGame()
    game.run()
