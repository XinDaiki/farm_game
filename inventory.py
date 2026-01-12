import pygame
from settings import *
from crop import Crop

class Inventory:
    def __init__(self):
        # Main inventory storage (36 slots)
        self.items = {
            "wheat_seed": INITIAL_SEEDS,
            "carrot_seed": 5,
            "tomato_seed": 3,
            "corn_seed": 2,
            "wheat": 0,
            "carrot": 0,
            "tomato": 0,
            "corn": 0,
            "wood": 0,
            "stone": 0,
        }
        
        # Hotbar (5 slots) - stores item names
        self.hotbar = ["wheat_seed", "carrot_seed", "tomato_seed", "corn_seed", None]
        self.selected_hotbar_slot = 0
        
        # UI state
        self.show_full_inventory = False
        self.selected_inventory_item = None
        
        # Fonts
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 16)
        
        # Item categories for display
        self.item_categories = {
            "Seeds": ["wheat_seed", "carrot_seed", "tomato_seed", "corn_seed"],
            "Crops": ["wheat", "carrot", "tomato", "corn"],
            "Resources": ["wood", "stone"],
            "Products": ["egg", "milk", "wool"],
            "Crafted": ["fence", "scarecrow", "chest"]
        }
        
    def add_item(self, item, amount=1):
        """Add item to inventory"""
        if item in self.items:
            self.items[item] += amount
        else:
            self.items[item] = amount
            
    def remove_item(self, item, amount=1):
        """Remove item from inventory"""
        if item in self.items and self.items[item] >= amount:
            self.items[item] -= amount
            return True
        return False
        
    def has_item(self, item, amount=1):
        """Check if inventory has item"""
        return self.items.get(item, 0) >= amount
        
    def use(self, item):
        """Use one of an item"""
        return self.remove_item(item, 1)
    
    def toggle_inventory(self):
        """Toggle full inventory display"""
        self.show_full_inventory = not self.show_full_inventory
        
    def get_selected_item(self):
        """Get currently selected item from hotbar"""
        selected_item = self.hotbar[self.selected_hotbar_slot]
        if selected_item and self.has_item(selected_item):
            return selected_item
        return None
    
    def get_selected_seed(self):
        """Get currently selected seed type from hotbar"""
        selected_item = self.get_selected_item()
        if selected_item and selected_item.endswith("_seed"):
            return selected_item.replace("_seed", "")
        return None
    
    def set_hotbar_slot(self, slot, item_name):
        """Set an item in a hotbar slot"""
        if 0 <= slot < 5:
            self.hotbar[slot] = item_name
    
    def handle_inventory_click(self, pos, screen_width, screen_height):
        """Handle clicks on the full inventory screen"""
        if not self.show_full_inventory:
            return False
        
        panel_width = min(600, screen_width - 40)
        panel_height = min(600, screen_height - 40)
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Check if click is inside panel
        if not (panel_x <= pos[0] <= panel_x + panel_width and 
                panel_y <= pos[1] <= panel_y + panel_height):
            hotbar_result = self.handle_integrated_hotbar_click(pos, panel_x, panel_y, panel_width, panel_height)
            if hotbar_result:
                return True
            return False
        
        # Check inventory grid clicks
        slot_size = min(70, (panel_width - 80) // 6)
        slots_per_row = 6
        start_x = panel_x + 30
        start_y = panel_y + 75
        slot_spacing = 10
        
        slot_index = 0
        all_items = list(self.items.keys())
        
        for row in range(6):
            for col in range(6):
                if slot_index >= len(all_items):
                    break
                
                x = start_x + col * (slot_size + slot_spacing)
                y = start_y + row * (slot_size + slot_spacing)
                
                if x <= pos[0] <= x + slot_size and y <= pos[1] <= y + slot_size:
                    item_name = all_items[slot_index]
                    count = self.items.get(item_name, 0)
                    
                    if count > 0:
                        self.selected_inventory_item = item_name
                        return True
                
                slot_index += 1
        
        hotbar_result = self.handle_integrated_hotbar_click(pos, panel_x, panel_y, panel_width, panel_height)
        if hotbar_result:
            return True
        
        return False
    
    def handle_integrated_hotbar_click(self, pos, panel_x, panel_y, panel_width, panel_height):
        """Handle clicks on integrated hotbar slots"""
        slot_size = 64
        spacing = 8
        total_width = (slot_size * 5) + (spacing * 4)
        start_x = panel_x + (panel_width - total_width) // 2
        start_y = panel_y + panel_height - slot_size - 30
        
        for i in range(5):
            x = start_x + i * (slot_size + spacing)
            y = start_y
            
            if x <= pos[0] <= x + slot_size and y <= pos[1] <= y + slot_size:
                if self.selected_inventory_item:
                    self.hotbar[i] = self.selected_inventory_item
                    self.selected_inventory_item = None
                    return True
                else:
                    self.selected_hotbar_slot = i
                    return True
        
        return False
    
    def handle_hotbar_click(self, pos, screen_width, screen_height):
        """Handle clicks on hotbar slots when inventory is closed"""
        slot_size = 64
        spacing = 8
        total_width = (slot_size * 5) + (spacing * 4)
        start_x = (screen_width - total_width) // 2
        start_y = screen_height - slot_size - 20
        
        for i in range(5):
            x = start_x + i * (slot_size + spacing)
            y = start_y
            
            if x <= pos[0] <= x + slot_size and y <= pos[1] <= y + slot_size:
                self.selected_hotbar_slot = i
                return True
        
        return False
    
    def draw_hotbar(self, surface, screen_width, screen_height):
        """Draw the hotbar at bottom center of screen"""
        slot_size = 64
        spacing = 8
        total_width = (slot_size * 5) + (spacing * 4)
        start_x = (screen_width - total_width) // 2
        start_y = screen_height - slot_size - 20
        
        for i in range(5):
            x = start_x + i * (slot_size + spacing)
            y = start_y
            
            is_selected = i == self.selected_hotbar_slot
            color = (100, 100, 100) if is_selected else (60, 60, 60)
            pygame.draw.rect(surface, color, (x, y, slot_size, slot_size))
            pygame.draw.rect(surface, WHITE if is_selected else GRAY, 
                           (x, y, slot_size, slot_size), 3 if is_selected else 2)
            
            item_name = self.hotbar[i]
            if item_name and item_name in self.items:
                count = self.items.get(item_name, 0)
                
                self.draw_item_icon(surface, item_name, x + slot_size // 2, y + 20)
                
                count_text = self.font.render(str(count), True, WHITE)
                text_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2))
                text_bg.fill((0, 0, 0))
                text_bg.set_alpha(180)
                surface.blit(text_bg, (x + 3, y + slot_size - 24))
                surface.blit(count_text, (x + 5, y + slot_size - 22))
                
                display_name = item_name.replace("_", " ").replace(" seed", "").title()
                if len(display_name) > 8:
                    display_name = display_name[:7] + "."
                name_text = self.small_font.render(display_name, True, WHITE)
                name_x = x + slot_size // 2 - name_text.get_width() // 2
                surface.blit(name_text, (name_x, y + 40))
            
            num_text = self.small_font.render(str(i + 1), True, YELLOW if is_selected else GRAY)
            surface.blit(num_text, (x + 4, y + 4))
    
    def draw_integrated_hotbar(self, surface, panel_x, panel_y, panel_width, panel_height):
        """Draw the hotbar integrated into the inventory panel"""
        slot_size = 64
        spacing = 8
        total_width = (slot_size * 5) + (spacing * 4)
        start_x = panel_x + (panel_width - total_width) // 2
        start_y = panel_y + panel_height - slot_size - 30
        
        hotbar_label = self.font.render("Hotbar", True, YELLOW)
        label_x = panel_x + (panel_width - hotbar_label.get_width()) // 2
        surface.blit(hotbar_label, (label_x, start_y - 25))
        
        for i in range(5):
            x = start_x + i * (slot_size + spacing)
            y = start_y
            
            is_selected = i == self.selected_hotbar_slot
            color = (100, 100, 100) if is_selected else (60, 60, 60)
            pygame.draw.rect(surface, color, (x, y, slot_size, slot_size))
            pygame.draw.rect(surface, WHITE if is_selected else GRAY, 
                           (x, y, slot_size, slot_size), 3 if is_selected else 2)
            
            item_name = self.hotbar[i]
            if item_name and item_name in self.items:
                count = self.items.get(item_name, 0)
                
                self.draw_item_icon(surface, item_name, x + slot_size // 2, y + 20)
                
                count_text = self.font.render(str(count), True, WHITE)
                text_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2))
                text_bg.fill((0, 0, 0))
                text_bg.set_alpha(180)
                surface.blit(text_bg, (x + 3, y + slot_size - 24))
                surface.blit(count_text, (x + 5, y + slot_size - 22))
                
                display_name = item_name.replace("_", " ").replace(" seed", "").title()
                if len(display_name) > 8:
                    display_name = display_name[:7] + "."
                name_text = self.small_font.render(display_name, True, WHITE)
                name_x = x + slot_size // 2 - name_text.get_width() // 2
                surface.blit(name_text, (name_x, y + 40))
            
            num_text = self.small_font.render(str(i + 1), True, YELLOW if is_selected else GRAY)
            surface.blit(num_text, (x + 4, y + 4))
    
    def draw_full_inventory(self, surface, screen_width, screen_height):
        """Draw the full inventory screen with integrated hotbar - responsive"""
        if not self.show_full_inventory:
            return
        
        # Draw semi-transparent background overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Responsive panel dimensions
        panel_width = min(600, screen_width - 40)
        panel_height = min(600, screen_height - 40)
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Draw panel background
        bg = pygame.Surface((panel_width, panel_height))
        bg.fill((40, 40, 40))
        surface.blit(bg, (panel_x, panel_y))
        
        pygame.draw.rect(surface, WHITE, (panel_x, panel_y, panel_width, panel_height), 3)
        
        title = self.title_font.render("Inventory", True, WHITE)
        surface.blit(title, (panel_x + 20, panel_y + 15))
        
        close_text = self.font.render("Press E to close", True, GRAY)
        surface.blit(close_text, (panel_x + panel_width - 150, panel_y + 15))
        
        if self.selected_inventory_item:
            instruction = self.small_font.render(
                f"Selected: {self.selected_inventory_item.replace('_', ' ').title()} - Click hotbar slot to assign",
                True, YELLOW
            )
        else:
            instruction = self.small_font.render(
                "Click item to select, then click hotbar slot to assign",
                True, GRAY
            )
        surface.blit(instruction, (panel_x + 20, panel_y + 45))
        
        # Draw inventory grid with responsive slot size
        slot_size = min(70, (panel_width - 80) // 6)
        slots_per_row = 6
        start_x = panel_x + 30
        start_y = panel_y + 75
        slot_spacing = 10
        
        slot_index = 0
        all_items = list(self.items.keys())
        
        for row in range(6):
            for col in range(6):
                if slot_index >= len(all_items):
                    break
                
                x = start_x + col * (slot_size + slot_spacing)
                y = start_y + row * (slot_size + slot_spacing)
                
                item_name = all_items[slot_index]
                count = self.items.get(item_name, 0)
                is_selected = item_name == self.selected_inventory_item
                
                slot_color = (80, 100, 80) if is_selected else (60, 60, 60)
                pygame.draw.rect(surface, slot_color, (x, y, slot_size, slot_size))
                border_color = YELLOW if is_selected else GRAY
                border_width = 3 if is_selected else 2
                pygame.draw.rect(surface, border_color, (x, y, slot_size, slot_size), border_width)
                
                if count > 0:
                    self.draw_item_icon(surface, item_name, x + slot_size // 2, y + 15)
                    
                    count_text = self.font.render(str(count), True, WHITE)
                    text_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2))
                    text_bg.fill((0, 0, 0))
                    text_bg.set_alpha(180)
                    surface.blit(text_bg, (x + 3, y + slot_size - 24))
                    surface.blit(count_text, (x + 5, y + slot_size - 22))
                    
                    display_name = item_name.replace("_", " ").title()
                    if len(display_name) > 9:
                        display_name = display_name[:8] + "."
                    name_text = self.small_font.render(display_name, True, WHITE)
                    name_x = x + slot_size // 2 - name_text.get_width() // 2
                    surface.blit(name_text, (name_x, y + 45))
                else:
                    display_name = item_name.replace("_", " ").title()
                    if len(display_name) > 9:
                        display_name = display_name[:8] + "."
                    name_text = self.small_font.render(display_name, True, (100, 100, 100))
                    name_x = x + slot_size // 2 - name_text.get_width() // 2
                    name_y = y + slot_size // 2 - name_text.get_height() // 2
                    surface.blit(name_text, (name_x, name_y))
                    
                    count_text = self.small_font.render("0", True, (100, 100, 100))
                    surface.blit(count_text, (x + 5, y + slot_size - 20))
                
                slot_index += 1
        
        separator_y = panel_y + panel_height - 120
        pygame.draw.line(surface, GRAY, (panel_x + 20, separator_y), (panel_x + panel_width - 20, separator_y), 2)
        
        self.draw_integrated_hotbar(surface, panel_x, panel_y, panel_width, panel_height)
    
    def draw_item_icon(self, surface, item_name, x, y):
        """Draw detailed icon for an item"""
        
        # Seeds
        if item_name == "wheat_seed":
            # Golden wheat seed
            pygame.draw.ellipse(surface, (218, 165, 32), (x - 6, y - 8, 12, 16))
            pygame.draw.ellipse(surface, (180, 130, 20), (x - 6, y - 8, 12, 16), 2)
            pygame.draw.line(surface, (150, 110, 15), (x - 2, y - 4), (x - 2, y + 4), 1)
            
        elif item_name == "carrot_seed":
            # Orange carrot seed
            pygame.draw.ellipse(surface, (255, 140, 0), (x - 6, y - 8, 12, 16))
            pygame.draw.ellipse(surface, (200, 100, 0), (x - 6, y - 8, 12, 16), 2)
            pygame.draw.circle(surface, (255, 180, 50), (x - 2, y - 2), 2)
            
        elif item_name == "tomato_seed":
            # Red tomato seed
            pygame.draw.ellipse(surface, (255, 50, 50), (x - 6, y - 8, 12, 16))
            pygame.draw.ellipse(surface, (200, 30, 30), (x - 6, y - 8, 12, 16), 2)
            pygame.draw.circle(surface, (255, 100, 100), (x + 2, y - 1), 2)
            
        elif item_name == "corn_seed":
            # Yellow corn seed
            pygame.draw.ellipse(surface, (255, 215, 0), (x - 6, y - 8, 12, 16))
            pygame.draw.ellipse(surface, (200, 170, 0), (x - 6, y - 8, 12, 16), 2)
            for i in range(3):
                pygame.draw.line(surface, (220, 185, 0), (x - 3, y - 4 + i * 3), (x + 3, y - 4 + i * 3), 1)
        
        # Crops
        elif item_name == "wheat":
            # Wheat bundle
            stem_x = x
            for i in range(3):
                offset = (i - 1) * 4
                pygame.draw.line(surface, (180, 130, 20), (stem_x + offset, y + 6), (stem_x + offset, y - 6), 2)
                pygame.draw.circle(surface, (218, 165, 32), (stem_x + offset, y - 8), 3)
            pygame.draw.rect(surface, (139, 69, 19), (x - 6, y + 6, 12, 3))
            
        elif item_name == "carrot":
            # Carrot with leaves
            pygame.draw.polygon(surface, (255, 140, 0), [(x, y + 8), (x - 5, y - 2), (x + 5, y - 2)])
            pygame.draw.polygon(surface, (200, 100, 0), [(x, y + 8), (x - 5, y - 2), (x + 5, y - 2)], 2)
            # Leaves
            pygame.draw.line(surface, (50, 150, 50), (x - 3, y - 2), (x - 6, y - 8), 2)
            pygame.draw.line(surface, (50, 150, 50), (x, y - 2), (x, y - 10), 2)
            pygame.draw.line(surface, (50, 150, 50), (x + 3, y - 2), (x + 6, y - 8), 2)
            
        elif item_name == "tomato":
            # Tomato with stem
            pygame.draw.circle(surface, (255, 50, 50), (x, y), 10)
            pygame.draw.circle(surface, (200, 30, 30), (x, y), 10, 2)
            pygame.draw.circle(surface, (255, 100, 100), (x - 3, y - 3), 3)
            # Stem
            pygame.draw.rect(surface, (50, 150, 50), (x - 1, y - 12, 2, 4))
            pygame.draw.circle(surface, (50, 180, 50), (x - 3, y - 11), 2)
            pygame.draw.circle(surface, (50, 180, 50), (x + 3, y - 11), 2)
            
        elif item_name == "corn":
            # Corn cob
            pygame.draw.ellipse(surface, (255, 215, 0), (x - 5, y - 10, 10, 20))
            pygame.draw.ellipse(surface, (200, 170, 0), (x - 5, y - 10, 10, 20), 2)
            for i in range(6):
                pygame.draw.line(surface, (230, 190, 0), (x - 3, y - 8 + i * 3), (x + 3, y - 8 + i * 3), 1)
            # Husk
            pygame.draw.line(surface, (150, 200, 100), (x - 6, y - 5), (x - 10, y - 10), 2)
            pygame.draw.line(surface, (150, 200, 100), (x + 6, y - 5), (x + 10, y - 10), 2)
        
        # Resources
        elif item_name == "wood":
            # Wood plank with grain
            pygame.draw.rect(surface, (139, 69, 19), (x - 10, y - 8, 20, 16))
            pygame.draw.rect(surface, (101, 50, 15), (x - 10, y - 8, 20, 16), 2)
            # Wood grain lines
            for i in range(3):
                y_offset = y - 4 + i * 4
                pygame.draw.line(surface, (101, 50, 15), (x - 8, y_offset), (x + 8, y_offset), 1)
            # Wood rings
            pygame.draw.circle(surface, (180, 90, 30), (x - 4, y - 2), 3, 1)
            pygame.draw.circle(surface, (180, 90, 30), (x + 3, y + 2), 2, 1)
            
        elif item_name == "stone":
            # Stone with cracks
            points = [(x, y - 10), (x + 9, y - 2), (x + 7, y + 8), (x - 7, y + 8), (x - 9, y - 2)]
            pygame.draw.polygon(surface, (128, 128, 128), points)
            pygame.draw.polygon(surface, (80, 80, 80), points, 2)
            # Cracks/texture
            pygame.draw.line(surface, (100, 100, 100), (x - 4, y - 4), (x + 2, y), 1)
            pygame.draw.line(surface, (100, 100, 100), (x, y - 2), (x + 4, y + 4), 1)
            pygame.draw.circle(surface, (150, 150, 150), (x - 3, y + 2), 2)
        
        # Animal Products
        elif item_name == "egg":
            # Egg with speckles
            pygame.draw.ellipse(surface, (255, 255, 220), (x - 8, y - 10, 16, 20))
            pygame.draw.ellipse(surface, (230, 230, 200), (x - 8, y - 10, 16, 20), 2)
            # Speckles
            pygame.draw.circle(surface, (220, 200, 180), (x - 3, y - 3), 1)
            pygame.draw.circle(surface, (220, 200, 180), (x + 2, y + 1), 1)
            pygame.draw.circle(surface, (220, 200, 180), (x - 1, y + 4), 1)
            # Shine
            pygame.draw.circle(surface, (255, 255, 255), (x - 2, y - 5), 2)
            
        elif item_name == "milk":
            # Milk bottle
            pygame.draw.rect(surface, (255, 255, 255), (x - 6, y - 6, 12, 14))
            pygame.draw.rect(surface, (200, 200, 200), (x - 6, y - 6, 12, 14), 2)
            # Bottle neck
            pygame.draw.rect(surface, (230, 230, 230), (x - 3, y - 10, 6, 4))
            pygame.draw.rect(surface, (200, 200, 200), (x - 3, y - 10, 6, 4), 1)
            # Cap
            pygame.draw.rect(surface, (255, 200, 200), (x - 4, y - 12, 8, 2))
            # Milk level
            pygame.draw.line(surface, (240, 240, 240), (x - 4, y - 2), (x + 4, y - 2), 1)
            
        elif item_name == "wool":
            # Fluffy wool
            for offset_x, offset_y in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 0)]:
                pygame.draw.circle(surface, (245, 245, 245), (x + offset_x, y + offset_y), 4)
            for offset_x, offset_y in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 0)]:
                pygame.draw.circle(surface, (220, 220, 220), (x + offset_x, y + offset_y), 4, 1)
                
        elif item_name == "truffle":
            # Dark truffle
            pygame.draw.ellipse(surface, (60, 40, 30), (x - 8, y - 6, 16, 12))
            pygame.draw.ellipse(surface, (40, 20, 10), (x - 8, y - 6, 16, 12), 2)
            # Texture spots
            pygame.draw.circle(surface, (50, 30, 20), (x - 2, y - 1), 2)
            pygame.draw.circle(surface, (50, 30, 20), (x + 3, y + 1), 1)
            
        elif item_name == "cheese":
            # Yellow cheese wedge
            points = [(x - 8, y + 6), (x + 8, y + 6), (x + 2, y - 8)]
            pygame.draw.polygon(surface, (255, 220, 100), points)
            pygame.draw.polygon(surface, (220, 180, 60), points, 2)
            # Holes
            pygame.draw.circle(surface, (230, 200, 80), (x - 2, y + 2), 2)
            pygame.draw.circle(surface, (230, 200, 80), (x + 3, y - 1), 2)
            
        elif item_name == "duck_egg":
            # Slightly blue-tinted egg
            pygame.draw.ellipse(surface, (220, 240, 240), (x - 8, y - 10, 16, 20))
            pygame.draw.ellipse(surface, (200, 220, 220), (x - 8, y - 10, 16, 20), 2)
            pygame.draw.circle(surface, (255, 255, 255), (x - 2, y - 5), 2)
            
        elif item_name == "rabbit_foot":
            # Lucky rabbit foot
            pygame.draw.ellipse(surface, (200, 200, 200), (x - 4, y - 8, 8, 16))
            pygame.draw.ellipse(surface, (180, 180, 180), (x - 4, y - 8, 8, 16), 2)
            # Toes
            for toe_x in [-2, 2]:
                pygame.draw.circle(surface, (190, 190, 190), (x + toe_x, y + 8), 2)
            pygame.draw.circle(surface, (190, 190, 190), (x, y + 10), 2)
            
        elif item_name == "horseshoe":
            # U-shaped horseshoe
            pygame.draw.arc(surface, (150, 150, 150), (x - 8, y - 6, 16, 16), 0, 3.14, 3)
            pygame.draw.circle(surface, (130, 130, 130), (x - 6, y + 4), 2)
            pygame.draw.circle(surface, (130, 130, 130), (x + 6, y + 4), 2)
            
        elif item_name == "llama_wool":
            # Colorful llama wool
            for offset_x, offset_y in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 0)]:
                pygame.draw.circle(surface, (220, 200, 180), (x + offset_x, y + offset_y), 4)
            for offset_x, offset_y in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 0)]:
                pygame.draw.circle(surface, (200, 180, 160), (x + offset_x, y + offset_y), 4, 1)
                
        elif item_name == "turkey_feather":
            # Striped feather
            pygame.draw.ellipse(surface, (160, 82, 45), (x - 3, y - 10, 6, 20))
            pygame.draw.ellipse(surface, (120, 60, 30), (x - 3, y - 10, 6, 20), 1)
            # Stripes
            for i in range(4):
                pygame.draw.line(surface, (100, 60, 30), (x - 2, y - 8 + i * 4), (x + 2, y - 8 + i * 4), 1)
            # Feather tip
            pygame.draw.circle(surface, (180, 100, 50), (x, y - 10), 2)
        
        # Crafted items
        elif item_name == "fence":
            # Fence piece
            pygame.draw.rect(surface, (139, 69, 19), (x - 8, y - 2, 16, 3))
            pygame.draw.rect(surface, (139, 69, 19), (x - 8, y + 2, 16, 3))
            pygame.draw.rect(surface, (101, 50, 15), (x - 6, y - 8, 3, 16))
            pygame.draw.rect(surface, (101, 50, 15), (x + 3, y - 8, 3, 16))
            
        elif item_name == "scarecrow":
            # Scarecrow figure
            pygame.draw.rect(surface, (139, 69, 19), (x - 1, y - 6, 2, 12))
            pygame.draw.rect(surface, (139, 69, 19), (x - 8, y - 2, 16, 2))
            pygame.draw.circle(surface, (218, 165, 32), (x, y - 8), 4)
            pygame.draw.circle(surface, BLACK, (x - 2, y - 9), 1)
            pygame.draw.circle(surface, BLACK, (x + 2, y - 9), 1)
            
        elif item_name == "chest":
            # Wooden chest
            pygame.draw.rect(surface, (101, 67, 33), (x - 10, y - 6, 20, 14))
            pygame.draw.rect(surface, (80, 50, 25), (x - 10, y - 6, 20, 14), 2)
            pygame.draw.rect(surface, (139, 90, 43), (x - 2, y, 4, 3))
            pygame.draw.line(surface, (80, 50, 25), (x - 8, y - 4), (x + 8, y - 4), 1)
        
        # Default for unknown items
        else:
            pygame.draw.rect(surface, (150, 150, 150), (x - 10, y - 10, 20, 20))
            pygame.draw.rect(surface, WHITE, (x - 10, y - 10, 20, 20), 2)
            pygame.draw.line(surface, (200, 200, 200), (x - 6, y - 6), (x + 6, y + 6), 2)
            pygame.draw.line(surface, (200, 200, 200), (x - 6, y + 6), (x + 6, y - 6), 2)
    
    def draw(self, surface, screen_width, screen_height):
        """Draw inventory UI"""
        if self.show_full_inventory:
            self.draw_full_inventory(surface, screen_width, screen_height)
        else:
            self.draw_hotbar(surface, screen_width, screen_height)