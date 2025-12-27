import pygame
from settings import *

class Crop(pygame.sprite.Sprite):
    # Crop data: growth_time (seconds), sell_price, seed_cost
    CROP_DATA = {
        "wheat": {"growth_time": 15, "sell_price": 25, "seed_cost": 10, "color": (218, 165, 32)},
        "carrot": {"growth_time": 20, "sell_price": 35, "seed_cost": 15, "color": (255, 140, 0)},
        "tomato": {"growth_time": 25, "sell_price": 50, "seed_cost": 20, "color": (255, 50, 50)},
        "corn": {"growth_time": 30, "sell_price": 60, "seed_cost": 25, "color": (255, 215, 0)},
    }
    
    def __init__(self, pos, crop_type="wheat", current_time=0):
        super().__init__()
        
        self.crop_type = crop_type
        self.stage = 0  # 0-3 growth stages
        self.max_stage = 3
        self.growth_time = self.CROP_DATA[crop_type]["growth_time"]
        self.time_planted = current_time
        self.needs_water = False  # Start without needing water for first stage
        self.watered = True  # Consider newly planted crops as watered for initial growth
        self.ready_to_harvest = False
        
        # Create crop images for each stage
        self.images = self.create_crop_images()
        self.image = self.images[self.stage]
        self.rect = self.image.get_rect(topleft=pos)
        
    def create_crop_images(self):
        """Create visual representation of crop at different stages"""
        images = []
        color = self.CROP_DATA[self.crop_type]["color"]
        
        for stage in range(4):
            img = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            if stage == 0:  # Seed
                pygame.draw.circle(img, (139, 69, 19), (TILE_SIZE // 2, TILE_SIZE - 4), 3)
                
            elif stage == 1:  # Sprout
                # Small green sprout
                pygame.draw.line(img, (50, 150, 50), 
                               (TILE_SIZE // 2, TILE_SIZE - 2), 
                               (TILE_SIZE // 2, TILE_SIZE - 10), 2)
                pygame.draw.circle(img, (50, 200, 50), 
                                 (TILE_SIZE // 2, TILE_SIZE - 10), 3)
                                 
            elif stage == 2:  # Growing
                # Larger plant
                stem_x = TILE_SIZE // 2
                pygame.draw.line(img, (40, 120, 40), 
                               (stem_x, TILE_SIZE - 2), 
                               (stem_x, TILE_SIZE - 18), 3)
                # Leaves
                pygame.draw.circle(img, (50, 180, 50), 
                                 (stem_x - 6, TILE_SIZE - 12), 4)
                pygame.draw.circle(img, (50, 180, 50), 
                                 (stem_x + 6, TILE_SIZE - 12), 4)
                # Small crop forming
                pygame.draw.circle(img, color, 
                                 (stem_x, TILE_SIZE - 16), 3)
                                 
            else:  # Mature
                # Full grown plant
                stem_x = TILE_SIZE // 2
                pygame.draw.line(img, (40, 120, 40), 
                               (stem_x, TILE_SIZE - 2), 
                               (stem_x, TILE_SIZE - 24), 4)
                # Leaves
                pygame.draw.circle(img, (50, 180, 50), 
                                 (stem_x - 8, TILE_SIZE - 14), 5)
                pygame.draw.circle(img, (50, 180, 50), 
                                 (stem_x + 8, TILE_SIZE - 14), 5)
                pygame.draw.circle(img, (50, 200, 50), 
                                 (stem_x, TILE_SIZE - 20), 6)
                # Mature crop
                pygame.draw.circle(img, color, 
                                 (stem_x, TILE_SIZE - 22), 6)
                pygame.draw.circle(img, color, 
                                 (stem_x - 5, TILE_SIZE - 18), 4)
                pygame.draw.circle(img, color, 
                                 (stem_x + 5, TILE_SIZE - 18), 4)
                # Shine effect when ready
                pygame.draw.circle(img, (255, 255, 200), 
                                 (stem_x + 3, TILE_SIZE - 24), 2)
                                 
            images.append(img)
        return images
        
    def water(self):
        """Water the crop"""
        if not self.watered:
            self.watered = True
            self.needs_water = False
            return True
        return False
        
    def update(self, current_time):
        """Update crop growth"""
        # Calculate growth progress
        time_since_planted = current_time - self.time_planted
        
        # If not watered, grow at 50% speed after stage 1
        growth_multiplier = 1.0
        if not self.watered and self.stage >= 1:
            growth_multiplier = 0.5
            
        adjusted_time = time_since_planted * growth_multiplier
        growth_per_stage = self.growth_time / self.max_stage
        new_stage = min(int(adjusted_time / growth_per_stage), self.max_stage)
        
        # Update stage
        if new_stage > self.stage:
            self.stage = new_stage
            self.image = self.images[self.stage]
            # Need water for optimal next stage growth
            if self.stage < self.max_stage:
                self.needs_water = True
                self.watered = False
                
        # Check if ready to harvest
        if self.stage >= self.max_stage:
            self.ready_to_harvest = True
            
    def draw_status(self, surface):
        """Draw status indicators above crop"""
        if self.ready_to_harvest:
            # Draw sparkle when ready to harvest
            import pygame
            from settings import YELLOW
            pygame.draw.circle(surface, YELLOW, 
                             (self.rect.centerx, self.rect.top - 5), 3)
        elif self.needs_water and self.stage > 0:
            # Draw water drop when needs water
            import pygame
            from settings import BLUE
            pygame.draw.circle(surface, BLUE, 
                             (self.rect.centerx, self.rect.top - 5), 3)
            pygame.draw.circle(surface, (150, 200, 255), 
                             (self.rect.centerx, self.rect.top - 7), 2)
            
    def harvest(self):
        """Harvest the crop and return sell price"""
        if self.ready_to_harvest:
            return self.CROP_DATA[self.crop_type]["sell_price"]
        return 0