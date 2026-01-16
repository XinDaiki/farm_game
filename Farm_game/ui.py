import pygame
from settings import *

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(Arial, 14)
        self.title_font = pygame.font.SysFont(Arial, 20)
        self.small_font = pygame.font.SysFont(Arial, 14)
        self.tiny_font = pygame.font.SysFont(Arial, 12)
        
        # Settings
        self.show_controls = False
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def toggle_controls(self):
        """Toggle controls visibility"""
        self.show_controls = not self.show_controls
        if not self.show_controls:
            self.scroll_offset = 0
        
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
        """Draw scrollable controls guide"""
        if not self.show_controls:
            return
        
        # Control categories
        controls = {
            "Movement": [
                "WASD / Arrow Keys - Move player",
                "Mouse Scroll - Scroll controls (if needed)"
            ],
            "Tools & Actions": [
                "Left Click - Use current tool",
                "T - Cycle through tools",
                "Hand - Plant seeds / Harvest crops",
                "Hoe - Till soil on claimed plots",
                "Watering Can - Water crops/soil",
                "Axe - Chop trees for wood",
                "Scythe - Clear grass"
            ],
            "Plots & Land": [
                "Right Click (Grass) - Claim plot ($50)",
                "Right Click (Tilled) - Untill soil to grass",
                "Right Click (Claimed) - Sell plot ($40)",
                "L - Lock/Unlock claimed plot",
                "Must have Hoe to claim plots!"
            ],
            "Inventory & Crafting": [
                "1-5 - Select hotbar slot",
                "E - Open/Close inventory",
                "C - Open/Close crafting menu",
                "Click item in inventory to select",
                "Click hotbar slot to assign item"
            ],
            "Interactions": [
                "F - Interact with NPCs/Animals",
                "Near Shopkeeper - Buy/Sell items",
                "Near Animals - Feed/Collect products",
                "Animals need feeding after collection"
            ],
            "Quests & UI": [
                "Q - Open/Close quest log",
                "Click quest to view details",
                "Complete objectives to earn rewards",
                "Claim button appears when done"
            ],
            "Display & Settings": [
                "I - Toggle grid overlay",
                "H - Show shop help message",
                "Settings Button - Toggle this guide",
                "Mouse scroll - Scroll this guide"
            ],
            "Game Management": [
                "ESC - Save game and quit",
                "Auto-saves when closing shop",
                "Progress saved on exit"
            ],
            "Tips & Tricks": [
                "Claim plots before tilling!",
                "Water crops for faster growth",
                "Lock important plots to prevent selling",
                "Check quest log for objectives (Q)",
                "Sell crops to Shopkeeper for money",
                "Feed animals after collecting products",
                "Energy regenerates over time",
                "Different crops have different values"
            ]
        }
        
        # Calculate total content height
        line_height = 22
        category_spacing = 35
        total_height = 0
        for category, items in controls.items():
            total_height += category_spacing + (len(items) * line_height)
        
        # Panel dimensions
        panel_width = 420
        panel_height = min(screen_height - 100, 700)
        panel_x = screen_width - panel_width - 10
        panel_y = 50
        
        # Calculate max scroll
        content_height = total_height + 60  # Extra padding
        self.max_scroll = max(0, content_height - panel_height + 40)
        
        # Clamp scroll offset
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Background
        bg = pygame.Surface((panel_width, panel_height))
        bg.set_alpha(220)
        bg.fill((40, 40, 40))
        surface.blit(bg, (panel_x, panel_y))
        
        # Border
        pygame.draw.rect(surface, WHITE, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Create scrollable surface
        scroll_surface = pygame.Surface((panel_width - 20, content_height))
        scroll_surface.fill((40, 40, 40))
        
        # Title on main surface (non-scrolling)
        title = self.title_font.render("Controls & Guide", True, YELLOW)
        surface.blit(title, (panel_x + 15, panel_y + 12))
        
        # Close hint on main surface (non-scrolling)
        close_text = self.small_font.render("Click gear to close", True, GRAY)
        surface.blit(close_text, (panel_x + panel_width - 145, panel_y + 15))
        
        # Draw content on scroll surface
        y_pos = 10
        
        for category, items in controls.items():
            # Category header
            category_text = self.font.render(category, True, YELLOW)
            scroll_surface.blit(category_text, (10, y_pos))
            y_pos += 25
            
            # Category items
            for item in items:
                # Check if item is a tip (starts with specific patterns)
                is_tip = not any(char in item for char in ['-', ':'])
                color = (150, 200, 255) if is_tip else WHITE
                
                item_text = self.small_font.render(f"  • {item}", True, color)
                scroll_surface.blit(item_text, (10, y_pos))
                y_pos += line_height
            
            y_pos += 15  # Space between categories
        
        # Blit scrollable content with offset
        scroll_rect = pygame.Rect(10, 50, panel_width - 20, panel_height - 60)
        surface.set_clip((panel_x + 10, panel_y + 50, panel_width - 20, panel_height - 60))
        surface.blit(scroll_surface, (panel_x + 10, panel_y + 50 - self.scroll_offset))
        surface.set_clip(None)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = max(30, int((panel_height - 60) * (panel_height - 60) / content_height))
            scrollbar_y = panel_y + 50 + int((panel_height - 60 - scrollbar_height) * (self.scroll_offset / self.max_scroll))
            
            # Scrollbar track
            pygame.draw.rect(surface, (80, 80, 80), 
                           (panel_x + panel_width - 15, panel_y + 50, 10, panel_height - 60))
            # Scrollbar thumb
            pygame.draw.rect(surface, (150, 150, 150), 
                           (panel_x + panel_width - 15, scrollbar_y, 10, scrollbar_height))
            pygame.draw.rect(surface, WHITE, 
                           (panel_x + panel_width - 15, scrollbar_y, 10, scrollbar_height), 1)
            
            # Scroll hint
            if self.scroll_offset < self.max_scroll:
                hint = self.tiny_font.render("Scroll for more ↓", True, YELLOW)
                surface.blit(hint, (panel_x + panel_width - 110, panel_y + panel_height - 20))
    
    def handle_scroll(self, event, screen_width, screen_height):
        """Handle mouse wheel scrolling in controls panel"""
        if not self.show_controls:
            return False
        
        panel_width = 420
        panel_height = min(screen_height - 100, 700)
        panel_x = screen_width - panel_width - 10
        panel_y = 50
        
        # Check if mouse is over the controls panel
        mouse_pos = pygame.mouse.get_pos()
        if (panel_x <= mouse_pos[0] <= panel_x + panel_width and
            panel_y <= mouse_pos[1] <= panel_y + panel_height):
            
            if event.type == pygame.MOUSEWHEEL:
                # Scroll speed
                scroll_speed = 30
                self.scroll_offset -= event.y * scroll_speed
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                return True
        
        return False
    
    def draw_settings_button(self, surface, screen_width, screen_height):
        """Draw settings button in bottom-right corner"""
        button_size = 32
        button_x = screen_width - button_size - 10
        button_y = screen_height - button_size - 10
        
        # Button background
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        color = (80, 80, 80) if self.show_controls else (60, 60, 60)
        pygame.draw.rect(surface, color, button_rect)
        border_color = YELLOW if self.show_controls else WHITE
        pygame.draw.rect(surface, border_color, button_rect, 2)
        
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
            pygame.draw.line(surface, border_color, (x1, y1), (x2, y2), 2)
        
        # Center circle
        pygame.draw.circle(surface, color, (center_x, center_y), 6)
        pygame.draw.circle(surface, border_color, (center_x, center_y), 6, 2)
        pygame.draw.circle(surface, color, (center_x, center_y), 3)
        
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
