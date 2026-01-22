import pygame
from settings import *
from crop import Crop

class NPC(pygame.sprite.Sprite):
    NPC_DATA = {
        "shopkeeper": {
            "color": (150, 75, 0),
            "dialogues": [
                "Welcome to my shop!",
                "Need some seeds?",
                "Fresh supplies daily!",
                "How's the farm going?"
            ],
            "shop": True
        },
        "mayor": {
            "color": (50, 50, 150),
            "dialogues": [
                "Welcome to our village!",
                "The harvest festival is coming!",
                "Keep up the good work!",
                "We're proud of our farmers!"
            ],
            "shop": False
        },
        "fisherman": {
            "color": (100, 150, 200),
            "dialogues": [
                "The fish are biting today!",
                "Have you tried fishing?",
                "I caught a big one yesterday!",
                "The lake is beautiful this time of year."
            ],
            "shop": False
        }
    }
    
    def __init__(self, pos, npc_type="shopkeeper"):
        super().__init__()
        
        self.npc_type = npc_type
        self.data = self.NPC_DATA[npc_type]
        
        # Create NPC sprite
        self.image = pygame.Surface((28, 32))
        self.create_sprite()
        
        self.rect = self.image.get_rect(center=pos)
        
        # Dialogue
        self.current_dialogue = 0
        self.dialogue_visible = False
        self.dialogue_timer = 0
        self.font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 24)
        
        # Shop state
        self.shop_mode = None  # None, 'menu', 'buy', or 'sell'
        
    def create_sprite(self):
        """Create NPC visual representation"""
        color = self.data["color"]
        
        # Body
        self.image.fill((255, 200, 150))  # Skin
        pygame.draw.rect(self.image, color, (6, 8, 16, 12))  # Shirt
        pygame.draw.rect(self.image, (50, 50, 50), (6, 20, 16, 12))  # Pants
        
        # Head
        pygame.draw.circle(self.image, (255, 220, 177), (14, 6), 6)
        pygame.draw.circle(self.image, BLACK, (11, 5), 2)  # Left eye
        pygame.draw.circle(self.image, BLACK, (17, 5), 2)  # Right eye
        pygame.draw.line(self.image, BLACK, (12, 8), (16, 8), 1)  # Smile
        
        # Hat (for shopkeeper)
        if self.npc_type == "shopkeeper":
            pygame.draw.rect(self.image, color, (8, 0, 12, 4))
            pygame.draw.rect(self.image, color, (6, 3, 16, 2))
            
        # Fishing rod (for fisherman)
        if self.npc_type == "fisherman":
            pygame.draw.line(self.image, BROWN, (24, 12), (28, 2), 2)
            
    def talk(self):
        """Start dialogue with NPC"""
        if self.npc_type == "shopkeeper":
            self.shop_mode = 'menu'
            return "Hello! What can I do for you today?"
        else:
            self.dialogue_visible = True
            self.dialogue_timer = 180  # Show for 3 seconds at 60 FPS
            dialogue = self.data["dialogues"][self.current_dialogue]
            self.current_dialogue = (self.current_dialogue + 1) % len(self.data["dialogues"])
            return dialogue
        
    def update(self, dt):
        """Update NPC"""
        if self.dialogue_visible:
            self.dialogue_timer -= 1
            if self.dialogue_timer <= 0:
                self.dialogue_visible = False
                
    def draw_dialogue(self, surface):
        """Draw dialogue bubble"""
        if self.dialogue_visible and self.npc_type != "shopkeeper":
            dialogue = self.data["dialogues"][self.current_dialogue - 1]
            
            # Create dialogue box
            padding = 10
            text_surface = self.font.render(dialogue, True, BLACK)
            box_width = text_surface.get_width() + padding * 2
            box_height = text_surface.get_height() + padding * 2
            
            # Position above NPC
            box_x = self.rect.centerx - box_width // 2
            box_y = self.rect.top - box_height - 10
            
            # Keep on screen (use world surface dimensions)
            world_width = TILE_SIZE * MAP_WIDTH
            world_height = TILE_SIZE * MAP_HEIGHT
            box_x = max(5, min(box_x, world_width - box_width - 5))
            box_y = max(5, box_y)
            
            # Draw box
            pygame.draw.rect(surface, WHITE, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, BLACK, (box_x, box_y, box_width, box_height), 2)
            
            # Draw pointer
            points = [
                (self.rect.centerx, self.rect.top - 5),
                (self.rect.centerx - 5, box_y + box_height),
                (self.rect.centerx + 5, box_y + box_height)
            ]
            pygame.draw.polygon(surface, WHITE, points)
            pygame.draw.lines(surface, BLACK, True, points, 2)
            
            # Draw text
            surface.blit(text_surface, (box_x + padding, box_y + padding))
            
    def draw_label(self, surface):
        """Draw name label above NPC"""
        if self.npc_type == "shopkeeper":
            label_font = pygame.font.Font(None, 16)
            label = label_font.render("SHOP", True, (255, 215, 0))
            label_bg = pygame.Surface((label.get_width() + 6, label.get_height() + 4))
            label_bg.fill((0, 0, 0))
            label_bg.set_alpha(180)
            
            label_x = self.rect.centerx - label.get_width() // 2 - 3
            label_y = self.rect.top - 20
            
            surface.blit(label_bg, (label_x, label_y))
            surface.blit(label, (label_x + 3, label_y + 2))
    
    def draw_shop_menu(self, surface, screen_width, screen_height):
        """Draw the initial shop menu with Buy/Sell options"""
        if self.shop_mode != 'menu':
            return
        
        menu_width = 400
        menu_height = 280
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2
        
        # Background
        bg = pygame.Surface((menu_width, menu_height))
        bg.set_alpha(240)
        bg.fill((60, 40, 20))
        surface.blit(bg, (menu_x, menu_y))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = self.title_font.render("Shopkeeper's Store", True, YELLOW)
        surface.blit(title, (menu_x + 20, menu_y + 15))
        
        # Greeting
        greeting = self.font.render("Hello there! What would you like to do?", True, WHITE)
        surface.blit(greeting, (menu_x + 20, menu_y + 55))
        
        # Buy button
        buy_rect = pygame.Rect(menu_x + 40, menu_y + 100, menu_width - 80, 50)
        pygame.draw.rect(surface, (80, 120, 80), buy_rect)
        pygame.draw.rect(surface, WHITE, buy_rect, 3)
        buy_text = self.title_font.render("BUY SEEDS", True, WHITE)
        buy_x = buy_rect.centerx - buy_text.get_width() // 2
        buy_y = buy_rect.centery - buy_text.get_height() // 2
        surface.blit(buy_text, (buy_x, buy_y))
        
        # Sell button
        sell_rect = pygame.Rect(menu_x + 40, menu_y + 165, menu_width - 80, 50)
        pygame.draw.rect(surface, (120, 80, 80), sell_rect)
        pygame.draw.rect(surface, WHITE, sell_rect, 3)
        sell_text = self.title_font.render("SELL CROPS", True, WHITE)
        sell_x = sell_rect.centerx - sell_text.get_width() // 2
        sell_y = sell_rect.centery - sell_text.get_height() // 2
        surface.blit(sell_text, (sell_x, sell_y))
        
        # Close instruction
        close_text = self.font.render("Right-click or ESC to close", True, GRAY)
        surface.blit(close_text, (menu_x + 20, menu_y + menu_height - 30))
    
    def draw_buy_menu(self, surface, player_money, screen_width, screen_height):
        """Draw the buy seeds menu"""
        if self.shop_mode != 'buy':
            return
        
        shop_items = self.get_shop_items()
        
        menu_width = 400
        menu_height = 380
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2
        
        # Background
        bg = pygame.Surface((menu_width, menu_height))
        bg.set_alpha(240)
        bg.fill((60, 40, 20))
        surface.blit(bg, (menu_x, menu_y))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = self.title_font.render("Buy Seeds", True, YELLOW)
        surface.blit(title, (menu_x + 20, menu_y + 10))
        
        # Money display
        money = self.font.render(f"Your Money: ${player_money}", True, WHITE)
        surface.blit(money, (menu_x + 20, menu_y + 40))
        
        # Items
        y_offset = 80
        for item, price in shop_items.items():
            y = menu_y + y_offset
            
            # Item box
            item_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 40)
            can_buy = player_money >= price
            color = (80, 60, 40) if can_buy else (60, 40, 30)
            pygame.draw.rect(surface, color, item_rect)
            pygame.draw.rect(surface, WHITE if can_buy else GRAY, item_rect, 2)
            
            # Item name
            name = item.replace("_", " ").title()
            name_text = self.font.render(name, True, WHITE)
            surface.blit(name_text, (item_rect.x + 10, item_rect.y + 10))
            
            # Price
            price_text = self.font.render(f"${price}", True, YELLOW if can_buy else GRAY)
            surface.blit(price_text, (item_rect.right - 80, item_rect.y + 10))
            
            y_offset += 50
        
        # Back button
        back_rect = pygame.Rect(menu_x + 40, menu_y + menu_height - 70, 100, 35)
        pygame.draw.rect(surface, (100, 100, 100), back_rect)
        pygame.draw.rect(surface, WHITE, back_rect, 2)
        back_text = self.font.render("BACK", True, WHITE)
        back_x = back_rect.centerx - back_text.get_width() // 2
        back_y = back_rect.centery - back_text.get_height() // 2
        surface.blit(back_text, (back_x, back_y))
        
        # Instructions
        instructions = self.font.render("Click item to buy", True, WHITE)
        surface.blit(instructions, (menu_x + 20, menu_y + menu_height - 30))
    
    def draw_sell_menu(self, surface, inventory, player_money, screen_width, screen_height):
        """Draw the sell crops menu"""
        if self.shop_mode != 'sell':
            return
        
        # Get sellable items from inventory
        sellable_items = self.get_sellable_items(inventory)
        
        menu_width = 450
        menu_height = 450
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2
        
        # Background
        bg = pygame.Surface((menu_width, menu_height))
        bg.set_alpha(240)
        bg.fill((60, 40, 20))
        surface.blit(bg, (menu_x, menu_y))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = self.title_font.render("Sell Crops & Products", True, YELLOW)
        surface.blit(title, (menu_x + 20, menu_y + 10))
        
        # Money display
        money = self.font.render(f"Your Money: ${player_money}", True, WHITE)
        surface.blit(money, (menu_x + 20, menu_y + 40))
        
        # Items
        if not sellable_items:
            no_items = self.font.render("You don't have any crops or products to sell!", True, WHITE)
            surface.blit(no_items, (menu_x + 40, menu_y + 100))
        else:
            y_offset = 80
            for item, (count, price) in sellable_items.items():
                y = menu_y + y_offset
                
                # Item box
                item_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 40)
                pygame.draw.rect(surface, (80, 60, 40), item_rect)
                pygame.draw.rect(surface, WHITE, item_rect, 2)
                
                # Item name and count
                name = item.replace("_", " ").title()
                name_text = self.font.render(f"{name} x{count}", True, WHITE)
                surface.blit(name_text, (item_rect.x + 10, item_rect.y + 10))
                
                # Price
                price_text = self.font.render(f"${price} each", True, YELLOW)
                surface.blit(price_text, (item_rect.right - 100, item_rect.y + 10))
                
                y_offset += 50
        
        # Sell All button
        if sellable_items:
            sell_all_rect = pygame.Rect(menu_x + menu_width - 150, menu_y + menu_height - 70, 110, 35)
            pygame.draw.rect(surface, (80, 120, 80), sell_all_rect)
            pygame.draw.rect(surface, WHITE, sell_all_rect, 2)
            sell_all_text = self.font.render("SELL ALL", True, WHITE)
            sell_all_x = sell_all_rect.centerx - sell_all_text.get_width() // 2
            sell_all_y = sell_all_rect.centery - sell_all_text.get_height() // 2
            surface.blit(sell_all_text, (sell_all_x, sell_all_y))
        
        # Back button
        back_rect = pygame.Rect(menu_x + 40, menu_y + menu_height - 70, 100, 35)
        pygame.draw.rect(surface, (100, 100, 100), back_rect)
        pygame.draw.rect(surface, WHITE, back_rect, 2)
        back_text = self.font.render("BACK", True, WHITE)
        back_x = back_rect.centerx - back_text.get_width() // 2
        back_y = back_rect.centery - back_text.get_height() // 2
        surface.blit(back_text, (back_x, back_y))
        
        # Instructions
        instructions = self.font.render("Click item to sell one, or SELL ALL", True, WHITE)
        surface.blit(instructions, (menu_x + 20, menu_y + menu_height - 30))
    
    def get_shop_items(self):
        """Return shop inventory"""
        if self.data["shop"]:
            return {
                "wheat_seed": 50,
                "carrot_seed": 125,
                "tomato_seed": 150,
                "corn_seed": 200,
            }
        return None
    
    def get_sellable_items(self, inventory):
        """Get items that can be sold with their prices"""
        sellable = {}
        
        # Crops with sell prices from Crop.CROP_DATA
        for crop_name, crop_data in Crop.CROP_DATA.items():
            if inventory.has_item(crop_name):
                count = inventory.items.get(crop_name, 0)
                if count > 0:
                    sellable[crop_name] = (count, crop_data["sell_price"])
        
        # Animal products
        animal_products = {
            "egg": 15,
            "milk": 25,
            "wool": 30
        }
        
        for product, price in animal_products.items():
            if inventory.has_item(product):
                count = inventory.items.get(product, 0)
                if count > 0:
                    sellable[product] = (count, price)
        
        return sellable
    
    def handle_shop_click(self, pos, player, inventory, screen_width, screen_height):
        """Handle clicks in shop interface - returns (action, result, message)"""
        menu_width = 400
        menu_x = (screen_width - menu_width) // 2
        
        # Handle menu selection
        if self.shop_mode == 'menu':
            menu_y = (screen_height - 280) // 2
            buy_rect = pygame.Rect(menu_x + 40, menu_y + 100, menu_width - 80, 50)
            sell_rect = pygame.Rect(menu_x + 40, menu_y + 165, menu_width - 80, 50)
            
            if buy_rect.collidepoint(pos):
                self.shop_mode = 'buy'
                return ('switch', True, "")
            elif sell_rect.collidepoint(pos):
                self.shop_mode = 'sell'
                return ('switch', True, "")
        
        # Handle buy menu
        elif self.shop_mode == 'buy':
            menu_y = (screen_height - 380) // 2
            shop_items = self.get_shop_items()
            
            # Check back button
            back_rect = pygame.Rect(menu_x + 40, menu_y + 380 - 70, 100, 35)
            if back_rect.collidepoint(pos):
                self.shop_mode = 'menu'
                return ('switch', True, "")
            
            # Check item purchases
            y_offset = 80
            for item, price in shop_items.items():
                y = menu_y + y_offset
                item_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 40)
                
                if item_rect.collidepoint(pos):
                    if player.money >= price:
                        player.money -= price
                        inventory.add_item(item, 1)
                        return ('buy', True, f"Bought {item.replace('_', ' ')}!")
                    else:
                        return ('buy', False, "Not enough money!")
                        
                y_offset += 50
        
        # Handle sell menu
        elif self.shop_mode == 'sell':
            menu_width = 450
            menu_x = (screen_width - menu_width) // 2
            menu_y = (screen_height - 450) // 2
            sellable_items = self.get_sellable_items(inventory)
            
            # Check back button
            back_rect = pygame.Rect(menu_x + 40, menu_y + 450 - 70, 100, 35)
            if back_rect.collidepoint(pos):
                self.shop_mode = 'menu'
                return ('switch', True, "")
            
            # Check sell all button
            if sellable_items:
                sell_all_rect = pygame.Rect(menu_x + menu_width - 150, menu_y + 450 - 70, 110, 35)
                if sell_all_rect.collidepoint(pos):
                    total_value = 0
                    items_sold = []
                    for item, (count, price) in sellable_items.items():
                        value = count * price
                        total_value += value
                        inventory.remove_item(item, count)
                        items_sold.append(f"{count} {item}")
                    
                    player.money += total_value
                    return ('sell', True, f"Sold all items for ${total_value}!")
            
            # Check individual item sales
            y_offset = 80
            for item, (count, price) in sellable_items.items():
                y = menu_y + y_offset
                item_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 40)
                
                if item_rect.collidepoint(pos):
                    inventory.remove_item(item, 1)
                    player.money += price
                    return ('sell', True, f"Sold {item.replace('_', ' ')} for ${price}!")
                    
                y_offset += 50
        
        return ('none', False, "")