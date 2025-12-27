import pygame
from settings import *
from crop import Crop

class Inventory:
    def __init__(self):
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
        self.selected_slot = 0
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 24)
        
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
        
    def get_selected_seed(self):
        """Get currently selected seed type"""
        seeds = ["wheat_seed", "carrot_seed", "tomato_seed", "corn_seed"]
        if self.selected_slot < len(seeds):
            seed = seeds[self.selected_slot]
            if self.has_item(seed):
                return seed.replace("_seed", "")
        return None
        
    def draw(self, surface):
        """Draw inventory UI"""
        # Draw semi-transparent background
        ui_rect = pygame.Rect(10, SCREEN_HEIGHT - 120, 400, 110)
        ui_surface = pygame.Surface((ui_rect.width, ui_rect.height))
        ui_surface.set_alpha(200)
        ui_surface.fill((40, 40, 40))
        surface.blit(ui_surface, ui_rect.topleft)
        
        # Draw title
        title = self.title_font.render("Inventory", True, WHITE)
        surface.blit(title, (20, SCREEN_HEIGHT - 115))
        
        # Draw seed slots
        seeds = [
            ("wheat_seed", "Wheat"),
            ("carrot_seed", "Carrot"),
            ("tomato_seed", "Tomato"),
            ("corn_seed", "Corn")
        ]
        
        slot_size = 60
        start_x = 20
        start_y = SCREEN_HEIGHT - 85
        
        for i, (seed_id, name) in enumerate(seeds):
            x = start_x + i * (slot_size + 10)
            y = start_y
            
            # Draw slot background
            color = (100, 100, 100) if i == self.selected_slot else (60, 60, 60)
            pygame.draw.rect(surface, color, (x, y, slot_size, slot_size))
            pygame.draw.rect(surface, WHITE if i == self.selected_slot else GRAY, 
                           (x, y, slot_size, slot_size), 2)
            
            # Draw seed icon
            seed_color = Crop.CROP_DATA.get(name.lower(), {}).get("color", WHITE)
            pygame.draw.circle(surface, seed_color, (x + slot_size // 2, y + 20), 8)
            
            # Draw quantity
            count = self.items.get(seed_id, 0)
            count_text = self.font.render(str(count), True, WHITE)
            surface.blit(count_text, (x + 5, y + slot_size - 20))
            
            # Draw name
            name_text = self.font.render(name[:5], True, WHITE)
            surface.blit(name_text, (x + 5, y + 35))
            
        # Draw resources
        resources = [
            ("wheat", "Wheat", (218, 165, 32)),
            ("carrot", "Carrot", (255, 140, 0)),
            ("tomato", "Tomato", (255, 50, 50)),
            ("corn", "Corn", (255, 215, 0)),
        ]
        
        res_x = 300
        res_y = SCREEN_HEIGHT - 85
        
        for i, (item_id, name, color) in enumerate(resources[:2]):
            y = res_y + i * 25
            
            # Draw icon
            pygame.draw.circle(surface, color, (res_x, y + 10), 6)
            
            # Draw name and count
            text = self.font.render(f"{name}: {self.items.get(item_id, 0)}", True, WHITE)
            surface.blit(text, (res_x + 15, y + 2))