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

class FarmGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Farm - Harvest Valley")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.world = World()
        self.world.create_default_map()
        
        # Animals
        self.animals = pygame.sprite.Group()
        self.animals.add(Animal((300, 300), "chicken"))
        self.animals.add(Animal((350, 320), "chicken"))
        self.animals.add(Animal((500, 400), "cow"))
        
        # NPCs
        self.npcs = pygame.sprite.Group()
        self.shopkeeper = NPC((100, 150), "shopkeeper")
        self.mayor = NPC((SCREEN_WIDTH - 100, 150), "mayor")
        self.npcs.add(self.shopkeeper, self.mayor)
        
        # Show welcome message
        self.show_notification("Welcome! Right-click Shopkeeper (brown vest) to buy seeds!")
        self.notification_timer = 300  # Show for 5 seconds
        
        # Systems
        self.inventory = Inventory()
        self.crafting = Crafting()
        self.time_system = TimeSystem()
        self.ui = UI()
        
        # Game state
        self.show_grid = False
        self.notification = ""
        self.notification_timer = 0
        self.shop_open = False
        self.paused = False
        
        self.font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                # Tool selection
                if event.key == pygame.K_t:
                    self.player.change_tool()
                    self.show_notification(f"Tool: {self.player.current_tool.replace('_', ' ').title()}")
                    
                # Seed selection
                elif event.key == pygame.K_1:
                    self.inventory.selected_slot = 0
                elif event.key == pygame.K_2:
                    self.inventory.selected_slot = 1
                elif event.key == pygame.K_3:
                    self.inventory.selected_slot = 2
                elif event.key == pygame.K_4:
                    self.inventory.selected_slot = 3
                    
                # Toggle systems
                elif event.key == pygame.K_c:
                    self.crafting.toggle_menu()
                elif event.key == pygame.K_i:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_h:
                    self.show_notification("Shopkeeper is in top-left area with 'SHOP' label!")
                    
                # Save and quit
                elif event.key == pygame.K_ESCAPE:
                    self.save_game()
                    pygame.quit()
                    sys.exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle crafting menu clicks
                if self.crafting.show_menu and event.button == 1:
                    if self.crafting.handle_click(mouse_pos, self.inventory):
                        self.show_notification("Item crafted!")
                        
                # Handle shop clicks
                elif self.shop_open and event.button == 1:
                    self.handle_shop_click(mouse_pos)
                    
                # Left click - use tool
                elif event.button == 1 and not self.crafting.show_menu:
                    self.use_tool(mouse_pos)
                    
                # Right click - interact
                elif event.button == 3:
                    if self.shop_open:
                        self.shop_open = False
                    else:
                        self.interact(mouse_pos)
                        
    def use_tool(self, pos):
        """Use the currently equipped tool"""
        tool = self.player.current_tool
        
        if tool == "hoe":
            # Till soil
            if self.player.use_energy(5):
                if self.world.till(pos):
                    self.show_notification("Soil tilled!")
                    
        elif tool == "watering_can":
            # Water crops and soil
            if self.player.use_energy(3):
                if self.world.water(pos):
                    self.show_notification("Watered!")
                    
        elif tool == "hand":
            # Plant or harvest
            crop_type = self.inventory.get_selected_seed()
            if crop_type:
                seed_name = f"{crop_type}_seed"
                if self.inventory.use(seed_name):
                    if self.world.plant(pos, crop_type):
                        self.show_notification(f"Planted {crop_type}!")
                    else:
                        # Refund seed if planting failed
                        self.inventory.add_item(seed_name, 1)
            else:
                # Try to harvest
                crop_type, value = self.world.harvest(pos)
                if crop_type:
                    self.inventory.add_item(crop_type, 1)
                    self.player.money += value
                    self.show_notification(f"Harvested {crop_type}! +${value}")
                    
        elif tool == "axe":
            # Chop trees for wood
            tile = self.world.get_tile_at_pos(pos)
            if tile and tile.kind == "T" and self.player.use_energy(10):
                self.inventory.add_item("wood", 3)
                self.show_notification("Chopped wood! +3 wood")
                
        elif tool == "scythe":
            # Clear grass
            tile = self.world.get_tile_at_pos(pos)
            if tile and tile.kind == "G" and self.player.use_energy(2):
                self.show_notification("Cleared grass!")
                
    def interact(self, pos):
        """Interact with NPCs and animals"""
        # Check NPCs
        for npc in self.npcs:
            if npc.rect.collidepoint(pos):
                dialogue = npc.talk()
                
                # Open shop if it's the shopkeeper
                if npc.npc_type == "shopkeeper":
                    self.shop_open = True
                return
                
        # Check animals
        for animal in self.animals:
            if animal.rect.collidepoint(pos):
                # Try to collect product
                product, value = animal.collect_product()
                if product:
                    self.inventory.add_item(product, 1)
                    self.player.money += value
                    self.show_notification(f"Collected {product}! +${value}")
                else:
                    # Feed animal
                    animal.feed()
                    self.show_notification(f"Fed {animal.animal_type}!")
                return
                
    def handle_shop_click(self, pos):
        """Handle clicks in shop interface"""
        shop_items = self.shopkeeper.open_shop()
        if not shop_items:
            return
            
        menu_width = 400
        menu_height = 350
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        y_offset = 80
        for item, price in shop_items.items():
            y = menu_y + y_offset
            item_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 40)
            
            if item_rect.collidepoint(pos):
                if self.player.money >= price:
                    self.player.money -= price
                    self.inventory.add_item(item, 1)
                    self.show_notification(f"Bought {item.replace('_', ' ')}!")
                else:
                    self.show_notification("Not enough money!")
                return
                
            y_offset += 50
            
    def show_notification(self, message):
        """Show a notification message"""
        self.notification = message
        self.notification_timer = 120  # 2 seconds at 60 FPS
        
    def update(self, dt):
        """Update all game systems"""
        if self.paused:
            return
            
        keys = pygame.key.get_pressed()
        
        # Update systems
        self.player.update(keys, dt)
        self.world.update()
        self.time_system.update(dt)
        
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
                
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw world
        self.world.tiles.draw(self.screen)
        
        # Draw grid if enabled
        if self.show_grid:
            self.world.draw_grid(self.screen)
            
        # Draw crops
        self.world.crops.draw(self.screen)
        
        # Draw crop status indicators
        for crop in self.world.crops:
            crop.draw_status(self.screen)
        
        # Draw animals
        self.animals.draw(self.screen)
        for animal in self.animals:
            animal.draw_status(self.screen)
            
        # Draw NPCs
        self.npcs.draw(self.screen)
        for npc in self.npcs:
            npc.draw_label(self.screen)
            npc.draw_dialogue(self.screen)
            
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        
        # Apply darkness for night
        if self.time_system.is_night():
            darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darkness.set_alpha(self.time_system.get_darkness_alpha())
            darkness.fill((0, 0, 40))
            self.screen.blit(darkness, (0, 0))
            
        # Draw UI
        self.ui.draw_player_stats(self.screen, self.player, self.time_system)
        self.ui.draw_controls(self.screen)
        self.inventory.draw(self.screen)
        
        # Draw crafting menu
        self.crafting.draw_menu(self.screen, self.inventory)
        
        # Draw shop
        if self.shop_open:
            shop_items = self.shopkeeper.open_shop()
            if shop_items:
                self.ui.draw_shop(self.screen, shop_items, self.player.money)
                
        # Draw notification
        if self.notification:
            self.ui.draw_notification(self.screen, self.notification)
            
        # Update display
        pygame.display.flip()
        
    def save_game(self):
        """Save game state"""
        save_data = {
            "player": {
                "pos": self.player.rect.center,
                "money": self.player.money,
                "energy": self.player.energy
            },
            "inventory": self.inventory.items,
            "time": {
                "time": self.time_system.time,
                "day": self.time_system.day,
                "season": self.time_system.season
            }
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
            
            # Restore time
            self.time_system.time = save_data["time"]["time"]
            self.time_system.day = save_data["time"]["day"]
            self.time_system.season = save_data["time"]["season"]
            
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
            dt = self.clock.tick(FPS) / 16.67  # Normalize to 60 FPS
            
            self.handle_events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    game = FarmGame()
    game.run()
