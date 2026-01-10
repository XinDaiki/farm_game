import pygame
from settings import *

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 18)
        self.tiny_font = pygame.font.Font(None, 14)
        
        # Settings
        self.show_controls = False
        
    def toggle_controls(self):
        """Toggle controls visibility"""
        self.show_controls = not self.show_controls
        
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
        
    def draw_controls(self, surface, screen_width, screen_height):
        """Draw controls guide"""
        if not self.show_controls:
            return
            
        controls = [
            "WASD/Arrows - Move",
            "Left Click - Use Tool",
            "Right Click - Claim/Sell",
            "L - Lock/Unlock Plot",
            "1-5 - Select Hotbar",
            "T - Change Tool",
            "E - Inventory",
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
        surface.blit(bg, (screen_width - 230, 10))
        
        # Border
        pygame.draw.rect(surface, WHITE, (screen_width - 230, 10, 220, bg_height), 2)
        
        # Title
        title = self.title_font.render("Controls", True, WHITE)
        surface.blit(title, (screen_width - 220, 20))
        
        # Controls list
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            surface.blit(text, (screen_width - 220, 50 + i * 22))
    
    def draw_settings_button(self, surface, screen_width, screen_height):
        """Draw settings button in bottom-right corner"""
        button_size = 32
        button_x = screen_width - button_size - 10
        button_y = screen_height - button_size - 10
        
        # Button background
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        pygame.draw.rect(surface, (60, 60, 60), button_rect)
        pygame.draw.rect(surface, WHITE, button_rect, 2)
        
        # Gear icon (simplified)
        center_x = button_x + button_size // 2
        center_y = button_y + button_size // 2
        
        # Draw gear teeth (8 spokes)
        import math
        for i in range(8):
            angle = i * 45 * math.pi / 180
            x1 = center_x + int(10 * math.cos(angle))
            y1 = center_y + int(10 * math.sin(angle))
            x2 = center_x + int(12 * math.cos(angle))
            y2 = center_y + int(12 * math.sin(angle))
            pygame.draw.line(surface, WHITE, (x1, y1), (x2, y2), 2)
        
        # Center circle
        pygame.draw.circle(surface, (60, 60, 60), (center_x, center_y), 6)
        pygame.draw.circle(surface, WHITE, (center_x, center_y), 6, 2)
        pygame.draw.circle(surface, (60, 60, 60), (center_x, center_y), 3)
        
        return button_rect
            
    def draw_notification(self, surface, message, screen_width, screen_height, duration=120):
        """Draw temporary notification"""
        if message:
            # Background
            text_surface = self.font.render(message, True, WHITE)
            padding = 20
            width = text_surface.get_width() + padding * 2
            height = text_surface.get_height() + padding * 2
            
            x = (screen_width - width) // 2
            y = screen_height - 200
            
            bg = pygame.Surface((width, height))
            bg.set_alpha(230)
            bg.fill((50, 50, 50))
            surface.blit(bg, (x, y))
            
            pygame.draw.rect(surface, YELLOW, (x, y, width, height), 3)
            
            surface.blit(text_surface, (x + padding, y + padding))
            
    def draw_shop(self, surface, shop_items, player_money, screen_width, screen_height):
        """Draw shop interface"""
        # Background
        menu_width = 400
        menu_height = 350
        menu_x = (screen_width - menu_width) // 2
        menu_y = (screen_height - menu_height) // 2
        
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