import pygame
from tile import Tile
from crop import Crop
from settings import *
import time

class World:
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.crops = pygame.sprite.Group()
        self.tile_map = {}  # Store tiles by grid position
        self.current_time = time.time()
        
    def load(self, filepath):
        """Load map from file"""
        try:
            with open(filepath) as f:
                for y, row in enumerate(f):
                    for x, tile_type in enumerate(row.strip()):
                        pos = (x * TILE_SIZE, y * TILE_SIZE)
                        tile = Tile(pos, tile_type)
                        self.tiles.add(tile)
                        self.tile_map[(x, y)] = tile
        except FileNotFoundError:
            # Create default map if file doesn't exist
            self.create_default_map()
            
    def create_default_map(self):
        """Create a default map layout"""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                
                # Create varied terrain
                if y < 3:  # Top border - trees
                    tile_type = "T" if x % 3 == 0 else "G"
                elif x < 2 or x > MAP_WIDTH - 3:  # Side borders
                    tile_type = "F"
                elif y > MAP_HEIGHT - 3:  # Bottom - water
                    tile_type = "W"
                elif 8 <= x <= 12 and 8 <= y <= 12:  # Center farm area
                    tile_type = "S"
                elif x % 4 == 0 and y % 4 == 0:  # Scattered rocks
                    tile_type = "R"
                elif (x + y) % 8 == 0:  # Paths
                    tile_type = "P"
                else:
                    tile_type = "G"
                    
                tile = Tile(pos, tile_type)
                self.tiles.add(tile)
                self.tile_map[(x, y)] = tile
                
    def get_tile_at_pos(self, pixel_pos):
        """Get tile at pixel position"""
        grid_x = pixel_pos[0] // TILE_SIZE 
        grid_y = pixel_pos[1] // TILE_SIZE
        return self.tile_map.get((grid_x, grid_y))
        
    def get_crop_at_pos(self, pixel_pos):
        """Get crop at pixel position"""
        for crop in self.crops:
            if crop.rect.collidepoint(pixel_pos):
                return crop
        return None
        
    def till(self, pixel_pos):
        """Till soil at position"""
        tile = self.get_tile_at_pos(pixel_pos)
        if tile:
            return tile.till()
        return False
        
    def water(self, pixel_pos):
        """Water tile at position"""
        tile = self.get_tile_at_pos(pixel_pos)
        if tile and tile.water():
            # Also water any crop on this tile
            crop = self.get_crop_at_pos(pixel_pos)
            if crop:
                crop.water()
            return True
        return False
        
    def plant(self, pixel_pos, crop_type):
        """Plant a seed at position"""
        grid_x = pixel_pos[0] // TILE_SIZE
        grid_y = pixel_pos[1] // TILE_SIZE
        tile = self.tile_map.get((grid_x, grid_y))
        
        # Check if tile is farmable and tilled
        if tile and tile.kind == "S":
            # Check if there's already a crop here
            tile_pos = (grid_x * TILE_SIZE, grid_y * TILE_SIZE)
            for crop in self.crops:
                if crop.rect.topleft == tile_pos:
                    return False  # Already has a crop
                    
            # Plant new crop
            crop = Crop(tile_pos, crop_type)
            crop.time_planted = self.current_time
            self.crops.add(crop)
            return True
        return False
        
    def harvest(self, pixel_pos):
        """Harvest crop at position"""
        crop = self.get_crop_at_pos(pixel_pos)
        if crop and crop.ready_to_harvest:
            value = crop.harvest()
            crop.kill()
            return crop.crop_type, value
        return None, 0
        
    def update(self):
        """Update world state"""
        self.current_time = time.time()
        
        # Update all crops
        for crop in self.crops:
            crop.update(self.current_time)
            
    def draw_grid(self, surface):
        """Draw grid lines for debugging"""
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (0, y), (SCREEN_WIDTH, y), 1)
