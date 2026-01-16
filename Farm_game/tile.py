import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, kind):
        super().__init__()
        self.kind = kind
        self.farmable = False
        self.watered = False
        
        # Create tile graphics
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        if kind == "G":  # Grass
            self.image.fill(GREEN)
            self.farmable = True
            # Add texture
            for _ in range(8):
                x = pygame.Rect(
                    pygame.math.Vector2(
                        pygame.math.Vector2(0, 0).x + (TILE_SIZE // 8) * (_ % 4),
                        pygame.math.Vector2(0, 0).y + (TILE_SIZE // 4) * (_ // 4)
                    ),
                    (2, 4)
                )
                pygame.draw.rect(self.image, DARK_GREEN, x)
                
        elif kind == "S":  # Soil/Tilled
            self.image.fill(BROWN)
            self.farmable = True
            self.tilled = True
            # Add lines for tilled look
            for i in range(4):
                pygame.draw.line(self.image, (100, 50, 10), 
                               (0, i * 8), (TILE_SIZE, i * 8), 1)
                               
        elif kind == "W":  # Water
            self.image.fill(BLUE)
            # Add wave effect
            pygame.draw.circle(self.image, (100, 180, 255), (8, 8), 4)
            pygame.draw.circle(self.image, (100, 180, 255), (24, 20), 3)
            
        elif kind == "P":  # Path
            self.image.fill(LIGHT_BROWN)
            # Add stones
            pygame.draw.circle(self.image, GRAY, (8, 8), 2)
            pygame.draw.circle(self.image, GRAY, (24, 20), 2)
            pygame.draw.circle(self.image, GRAY, (16, 24), 2)
            
        elif kind == "T":  # Tree
            self.image.fill(GREEN)
            # Draw tree trunk
            pygame.draw.rect(self.image, BROWN, (12, 16, 8, 16))
            # Draw tree canopy
            pygame.draw.circle(self.image, DARK_GREEN, (16, 12), 10)
            pygame.draw.circle(self.image, (50, 120, 50), (12, 10), 6)
            pygame.draw.circle(self.image, (50, 120, 50), (20, 10), 6)
            
        elif kind == "R":  # Rock
            self.image.fill(GREEN)
            pygame.draw.polygon(self.image, GRAY, 
                              [(16, 8), (26, 20), (16, 28), (6, 20)])
            pygame.draw.polygon(self.image, (100, 100, 100), 
                              [(16, 8), (26, 20), (16, 16)])
                              
        elif kind == "F":  # Fence
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, BROWN, (2, 12, 28, 4))
            pygame.draw.rect(self.image, BROWN, (2, 20, 28, 4))
            pygame.draw.rect(self.image, BROWN, (8, 8, 4, 20))
            pygame.draw.rect(self.image, BROWN, (20, 8, 4, 20))
            
        else:  # Default
            self.image.fill(BLACK)
            
        self.rect = self.image.get_rect(topleft=pos)
        
    def till(self):
        """Convert grass to tilled soil"""
        if self.kind == "G" and not self.watered:
            self.kind = "S"
            self.tilled = True
            self.image.fill(BROWN)
            for i in range(4):
                pygame.draw.line(self.image, (100, 50, 10), 
                               (0, i * 8), (TILE_SIZE, i * 8), 1)
            return True
        return False
        
    def water(self):
        """Water the tile"""
        if self.kind == "S" and not self.watered:
            self.watered = True
            self.image.fill((80, 50, 20))  # Darker, wet soil
            for i in range(4):
                pygame.draw.line(self.image, (60, 40, 15), 
                               (0, i * 8), (TILE_SIZE, i * 8), 1)
            return True
        return False
