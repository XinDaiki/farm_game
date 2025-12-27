import pygame
from settings import *

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 18)
        
    def draw_player_stats(self, surface, player, time_system):
        """Draw player stats in top-left corner"""
        # Background
        bg = pygame.Surface((250, 120))
        bg.set_alpha(200)
        bg.fill((40, 40, 40))
        surface.blit(bg, (10, 10))
        
        # Border
        pygame.draw.rect(surface, WHITE, (10, 10, 250, 120), 2)
        
        y_offset = 20
        
        # Money
        money_text = self.font.render(f"Money: ${player.money}", True, YELLOW)
        surface.blit(money_text, (20, y_offset))
        
        # Energy bar
        y_offset += 30
        energy_text = self.font.render(f"Energy:", True, WHITE)
        surface.blit(energy_text, (20, y_offset))
        
        bar_width = 150
        bar_height = 16
        bar_x = 100
        bar_y = y_offset + 2
        
        # Background bar
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Energy bar
        energy_width = int((player.energy / player.max_energy) * bar_width)
        energy_color = GREEN if player.energy > 30 else RED
        pygame.draw.rect(surface, energy_color, (bar_x, bar_y, energy_width, bar_height))
        # Border
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Current tool
        y_offset += 30
        tool_text = self.font.render(f"Tool: {player.current_tool.replace('_', ' ').title()}", 
                                     True, WHITE)
        surface.blit(tool_text, (20, y_offset))
        
        # Time and date
        y_offset += 30
        time_str = time_system.get_time_string()
        day_str = time_system.get_day_string()
        time_text = self.font.render(f"{day_str} - {time_str}", True, WHITE)
        surface.blit(time_text, (20, y_offset))
        
    def draw_controls(self, surface):
        """Draw controls guide"""
        controls = [
            "WASD/Arrows - Move",
            "Left Click - Use Tool",
            "Right Click - Interact",
            "1-4 - Select Seed",
            "T - Change Tool",
            "C - Crafting Menu",
            "I - Toggle Grid",
            "H - Shop Help",
            "ESC - Save & Quit"
        ]
        
        # Background
        bg_height = len(controls) * 22 + 30
        bg = pygame.Surface((220, bg_height))
        bg.set_alpha(200)
        bg.fill((40, 40, 40))
        surface.blit(bg, (SCREEN_WIDTH - 230, 10))
        
        # Border
        pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH - 230, 10, 220, bg_height), 2)
        
        # Title
        title = self.title_font.render("Controls", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH - 220, 20))
        
        # Controls list
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            surface.blit(text, (SCREEN_WIDTH - 220, 50 + i * 22))
            
    def draw_notification(self, surface, message, duration=120):
        """Draw temporary notification"""
        if message:
            # Background
            text_surface = self.font.render(message, True, WHITE)
            padding = 20
            width = text_surface.get_width() + padding * 2
            height = text_surface.get_height() + padding * 2
            
            x = (SCREEN_WIDTH - width) // 2
            y = SCREEN_HEIGHT - 200
            
            bg = pygame.Surface((width, height))
            bg.set_alpha(230)
            bg.fill((50, 50, 50))
            surface.blit(bg, (x, y))
            
            pygame.draw.rect(surface, YELLOW, (x, y, width, height), 3)
            
            surface.blit(text_surface, (x + padding, y + padding))
            
    def draw_shop(self, surface, shop_items, player_money):
        """Draw shop interface"""
        # Background
        menu_width = 400
        menu_height = 350
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        bg = pygame.Surface((menu_width, menu_height))
        bg.set_alpha(240)
        bg.fill((60, 40, 20))
        surface.blit(bg, (menu_x, menu_y))
        
        # Border
        pygame.draw.rect(surface, YELLOW, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = self.title_font.render("Shop", True, YELLOW)
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
            
        # Instructions
        instructions = self.small_font.render("Click item to buy | Right-click to close", 
                                              True, WHITE)
        surface.blit(instructions, (menu_x + 20, menu_y + menu_height - 30))
