import pygame
from settings import *

class Crafting:
    def __init__(self):
        self.recipes = {
            "fence": {
                "ingredients": {"wood": 5},
                "result": "fence",
                "amount": 1
            },
            "scarecrow": {
                "ingredients": {"wood": 10, "wheat": 5},
                "result": "scarecrow",
                "amount": 1
            },
            "chest": {
                "ingredients": {"wood": 20, "stone": 10},
                "result": "chest",
                "amount": 1
            },
        }
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 24)
        self.show_menu = False
        
    def can_craft(self, recipe_name, inventory):
        """Check if recipe can be crafted"""
        if recipe_name not in self.recipes:
            return False
            
        recipe = self.recipes[recipe_name]
        for ingredient, amount in recipe["ingredients"].items():
            if not inventory.has_item(ingredient, amount):
                return False
        return True
        
    def craft(self, recipe_name, inventory):
        """Craft an item"""
        if not self.can_craft(recipe_name, inventory):
            return False
            
        recipe = self.recipes[recipe_name]
        
        # Remove ingredients
        for ingredient, amount in recipe["ingredients"].items():
            inventory.remove_item(ingredient, amount)
            
        # Add result
        inventory.add_item(recipe["result"], recipe["amount"])
        return True
        
    def toggle_menu(self):
        """Toggle crafting menu"""
        self.show_menu = not self.show_menu
        
    def draw_menu(self, surface, inventory):
        """Draw crafting menu"""
        if not self.show_menu:
            return
            
        # Draw background
        menu_width = 400
        menu_height = 300
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        # Semi-transparent background
        bg = pygame.Surface((menu_width, menu_height))
        bg.set_alpha(230)
        bg.fill((40, 40, 40))
        surface.blit(bg, (menu_x, menu_y))
        
        # Border
        pygame.draw.rect(surface, WHITE, (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = self.title_font.render("Crafting", True, WHITE)
        surface.blit(title, (menu_x + 20, menu_y + 10))
        
        # Draw recipes
        y_offset = 50
        for i, (recipe_name, recipe) in enumerate(self.recipes.items()):
            y = menu_y + y_offset + i * 70
            
            # Recipe box
            recipe_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 60)
            can_craft = self.can_craft(recipe_name, inventory)
            color = (60, 80, 60) if can_craft else (80, 60, 60)
            pygame.draw.rect(surface, color, recipe_rect)
            pygame.draw.rect(surface, WHITE if can_craft else GRAY, recipe_rect, 2)
            
            # Recipe name
            name_text = self.font.render(recipe_name.capitalize(), True, WHITE)
            surface.blit(name_text, (recipe_rect.x + 10, recipe_rect.y + 5))
            
            # Ingredients
            ingredients_str = ", ".join([f"{amt} {ing}" for ing, amt in recipe["ingredients"].items()])
            ing_text = self.font.render(f"Needs: {ingredients_str}", True, WHITE)
            surface.blit(ing_text, (recipe_rect.x + 10, recipe_rect.y + 28))
            
            # Craft button hint
            if can_craft:
                hint = self.font.render("[Click to Craft]", True, YELLOW)
                surface.blit(hint, (recipe_rect.right - 120, recipe_rect.y + 28))
                
        # Close hint
        close_text = self.font.render("Press C to close", True, WHITE)
        surface.blit(close_text, (menu_x + 20, menu_y + menu_height - 30))
        
    def handle_click(self, pos, inventory):
        """Handle mouse click on crafting menu"""
        if not self.show_menu:
            return False
            
        menu_width = 400
        menu_height = 300
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        
        y_offset = 50
        for i, recipe_name in enumerate(self.recipes.keys()):
            y = menu_y + y_offset + i * 70
            recipe_rect = pygame.Rect(menu_x + 20, y, menu_width - 40, 60)
            
            if recipe_rect.collidepoint(pos):
                return self.craft(recipe_name, inventory)
                
        return False