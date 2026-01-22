import pygame
import os
from settings import *

class AssetManager:
    """
    Advanced asset manager with sprite sheet support.
    Handles loading, extracting, and scaling sprites from sprite sheets.
    """
    
    def __init__(self):
        self.assets_path = "assets"
        self.loaded_images = {}
        self.sprite_sheets = {}
        
        # Check if assets folder exists
        self.assets_available = os.path.exists(self.assets_path)
        
        if self.assets_available:
            print(f"✓ Assets found at '{self.assets_path}'")
            print(f"  Loading sprite sheets...")
            self._preload_sprite_sheets()
        else:
            print(f"⚠ Assets not found at '{self.assets_path}'")
            print(f"  Using procedural graphics as fallback.")
    
    def _preload_sprite_sheets(self):
        """Preload commonly used sprite sheets"""
        sprite_sheets = {
            'tileset': 'Tilemap/Tileset_Spring.png',
            'crops': 'Crops/Spring_Crops.png',
            'player_idle': 'Characters/Idle.png',
            'player_walk': 'Characters/Walk.png',
            'chicken': 'Animals/Chicken_Red.png',
            'cow': 'Animals/Female_Cow_Brown.png',
            'tree': 'Objects/Maple_Tree.png',
            'fence': 'Objects/Fence_s_copiar.png',
            'chest': 'Objects/chest.png',
        }
        
        for name, path in sprite_sheets.items():
            full_path = os.path.join(self.assets_path, path)
            if os.path.exists(full_path):
                try:
                    self.sprite_sheets[name] = pygame.image.load(full_path).convert_alpha()
                    print(f"  ✓ Loaded: {name}")
                except Exception as e:
                    print(f"  ✗ Error loading {name}: {e}")
    
    def extract_sprite(self, sheet_name, x, y, width, height, scale=2):
        """Extract a sprite from a sprite sheet"""
        if sheet_name not in self.sprite_sheets:
            return None
        
        sheet = self.sprite_sheets[sheet_name]
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, width, height))
        
        if scale != 1:
            sprite = pygame.transform.scale(sprite, (width * scale, height * scale))
        
        return sprite
    
    def get_tile_sprite(self, tile_type, size=TILE_SIZE):
        """Get tile sprite from tileset"""
        # Tileset_Spring.png layout (16x16 tiles)
        # Row 0: Various grass types
        # Row 1: Dirt/soil types
        # Row 2: Water and other
        
        tile_coords = {
            "G": (0, 0, 16, 16),      # Grass - top left
            "S": (0, 16, 16, 16),     # Soil/dirt - second row
            "W": (32, 32, 16, 16),    # Water - third row
            "P": (16, 0, 16, 16),     # Path - grass variant
        }
        
        if self.assets_available and tile_type in tile_coords:
            x, y, w, h = tile_coords[tile_type]
            sprite = self.extract_sprite('tileset', x, y, w, h, scale=2)
            if sprite:
                return sprite
        
        # Fallback for objects that aren't in tileset
        if tile_type == "T":  # Tree
            return self.get_tree_sprite(size)
        elif tile_type == "F":  # Fence
            return self.get_fence_sprite(size)
        elif tile_type == "R":  # Rock
            return self._create_rock_fallback(size)
        
        # Default fallback
        return self._create_tile_fallback(tile_type, size)
    
    def get_tree_sprite(self, size=TILE_SIZE):
        """Get tree sprite"""
        if 'tree' in self.sprite_sheets:
            # Maple tree is approximately 16x24, extract first frame
            sprite = self.extract_sprite('tree', 0, 0, 16, 24, scale=2)
            if sprite:
                # Scale to fit tile size
                return pygame.transform.scale(sprite, (size, size))
        return self._create_tree_fallback(size)
    
    def get_fence_sprite(self, size=TILE_SIZE):
        """Get fence sprite"""
        if 'fence' in self.sprite_sheets:
            sprite = self.extract_sprite('fence', 0, 0, 16, 16, scale=2)
            if sprite:
                return sprite
        return self._create_fence_fallback(size)
    
    def get_crop_sprites(self, crop_type):
        """Get crop sprite stages from Spring_Crops.png"""
        if 'crops' not in self.sprite_sheets:
            return None
        
        # Spring_Crops.png layout (16x16 per sprite)
        # Each crop has multiple growth stages
        # Approximate positions (adjust based on actual layout):
        crop_positions = {
            "wheat": [(0, 0), (16, 0), (32, 0), (48, 0)],      # Row 1, 4 stages
            "carrot": [(0, 16), (16, 16), (32, 16), (48, 16)],  # Row 2, 4 stages  
            "tomato": [(64, 0), (80, 0), (96, 0), (112, 0)],    # Row 1, later columns
            "corn": [(64, 16), (80, 16), (96, 16), (112, 16)],  # Row 2, later columns
        }
        
        if crop_type not in crop_positions:
            return None
        
        sprites = []
        for x, y in crop_positions[crop_type]:
            sprite = self.extract_sprite('crops', x, y, 16, 16, scale=2)
            if sprite:
                sprites.append(sprite)
        
        return sprites if len(sprites) == 4 else None
    
    def get_character_sprite(self, char_type, size=(28, 32)):
        """Get character sprite"""
        if char_type == "player":
            # Extract first frame of idle animation (16x16)
            if 'player_idle' in self.sprite_sheets:
                sprite = self.extract_sprite('player_idle', 0, 0, 16, 16, scale=2)
                if sprite:
                    return pygame.transform.scale(sprite, size)
        
        return None
    
    def get_animal_sprite(self, animal_type):
        """Get animal sprite"""
        animal_sheets = {
            "chicken": 'chicken',
            "cow": 'cow',
        }
        
        if animal_type in animal_sheets:
            sheet_name = animal_sheets[animal_type]
            if sheet_name in self.sprite_sheets:
                # Extract first frame (16x16 for chicken, might be different for cow)
                w, h = (16, 16) if animal_type == "chicken" else (16, 16)
                sprite = self.extract_sprite(sheet_name, 0, 0, w, h, scale=2)
                if sprite:
                    return sprite
        
        return None
    
    # Fallback creation methods
    def _create_tile_fallback(self, tile_type, size):
        """Create procedural tile graphics (fallback)"""
        img = pygame.Surface((size, size))
        
        if tile_type == "G":  # Grass
            img.fill(GREEN)
            for i in range(8):
                x = pygame.Rect((size // 8) * (i % 4), (size // 4) * (i // 4), 2, 4)
                pygame.draw.rect(img, DARK_GREEN, x)
        elif tile_type == "S":  # Soil
            img.fill(BROWN)
            for i in range(4):
                pygame.draw.line(img, (100, 50, 10), (0, i * 8), (size, i * 8), 1)
        elif tile_type == "W":  # Water
            img.fill(BLUE)
            pygame.draw.circle(img, (100, 180, 255), (8, 8), 4)
        elif tile_type == "P":  # Path
            img.fill(LIGHT_BROWN)
            pygame.draw.circle(img, GRAY, (8, 8), 2)
        else:
            img.fill(BLACK)
        
        return img
    
    def _create_tree_fallback(self, size):
        """Create fallback tree"""
        img = pygame.Surface((size, size))
        img.fill(GREEN)
        pygame.draw.rect(img, BROWN, (12, 16, 8, 16))
        pygame.draw.circle(img, DARK_GREEN, (16, 12), 10)
        return img
    
    def _create_fence_fallback(self, size):
        """Create fallback fence"""
        img = pygame.Surface((size, size))
        img.fill(GREEN)
        pygame.draw.rect(img, BROWN, (2, 12, 28, 4))
        pygame.draw.rect(img, BROWN, (8, 8, 4, 20))
        return img
    
    def _create_rock_fallback(self, size):
        """Create fallback rock"""
        img = pygame.Surface((size, size))
        img.fill(GREEN)
        pygame.draw.polygon(img, GRAY, [(16, 8), (26, 20), (16, 28), (6, 20)])
        return img

# Global asset manager instance
asset_manager = AssetManager()
