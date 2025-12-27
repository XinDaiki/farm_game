import pygame
import random
from settings import *

class Animal(pygame.sprite.Sprite):
    ANIMAL_TYPES = {
        "chicken": {
            "color": (255, 255, 255),
            "size": (20, 18),
            "product": "egg",
            "product_time": 30,
            "product_value": 15
        },
        "cow": {
            "color": (139, 90, 43),
            "size": (28, 24),
            "product": "milk",
            "product_time": 40,
            "product_value": 25
        },
        "sheep": {
            "color": (245, 245, 245),
            "size": (24, 20),
            "product": "wool",
            "product_time": 50,
            "product_value": 30
        }
    }
    
    def __init__(self, pos, animal_type="chicken"):
        super().__init__()
        
        self.animal_type = animal_type
        self.data = self.ANIMAL_TYPES[animal_type]
        
        # Create animal sprite
        width, height = self.data["size"]
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.create_sprite()
        
        self.rect = self.image.get_rect(center=pos)
        
        # Behavior
        self.speed = 1
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.change_direction_timer = 0
        self.change_direction_delay = random.randint(60, 180)
        
        # Production
        self.product_timer = 0
        self.has_product = False
        self.fed = True
        self.happiness = 100
        
    def create_sprite(self):
        """Create animal visual representation"""
        color = self.data["color"]
        width, height = self.data["size"]
        
        if self.animal_type == "chicken":
            # Body
            pygame.draw.ellipse(self.image, color, (2, 6, 16, 12))
            # Head
            pygame.draw.circle(self.image, color, (14, 6), 5)
            # Beak
            pygame.draw.polygon(self.image, (255, 165, 0), 
                              [(17, 6), (22, 5), (22, 7)])
            # Eye
            pygame.draw.circle(self.image, BLACK, (15, 5), 1)
            # Comb
            pygame.draw.circle(self.image, RED, (14, 2), 2)
            # Legs
            pygame.draw.line(self.image, (255, 165, 0), (8, 18), (8, 16), 2)
            pygame.draw.line(self.image, (255, 165, 0), (12, 18), (12, 16), 2)
            
        elif self.animal_type == "cow":
            # Body
            pygame.draw.ellipse(self.image, color, (2, 8, 24, 14))
            # Head
            pygame.draw.ellipse(self.image, color, (20, 6, 8, 10))
            # Spots
            pygame.draw.circle(self.image, BLACK, (8, 12), 3)
            pygame.draw.circle(self.image, BLACK, (16, 14), 2)
            # Eyes
            pygame.draw.circle(self.image, BLACK, (24, 9), 1)
            # Horns
            pygame.draw.line(self.image, (200, 200, 200), (22, 6), (20, 4), 2)
            pygame.draw.line(self.image, (200, 200, 200), (26, 6), (28, 4), 2)
            # Legs
            for x in [6, 10, 16, 20]:
                pygame.draw.line(self.image, color, (x, 22), (x, 20), 2)
                
        elif self.animal_type == "sheep":
            # Fluffy body
            pygame.draw.circle(self.image, color, (12, 12), 10)
            pygame.draw.circle(self.image, color, (8, 10), 6)
            pygame.draw.circle(self.image, color, (16, 10), 6)
            # Head (darker)
            pygame.draw.circle(self.image, (50, 50, 50), (18, 8), 4)
            # Eye
            pygame.draw.circle(self.image, BLACK, (19, 7), 1)
            # Legs
            for x in [6, 10, 14, 18]:
                pygame.draw.line(self.image, (50, 50, 50), (x, 20), (x, 18), 2)
                
    def update(self, dt):
        """Update animal behavior"""
        # Random movement
        self.change_direction_timer += 1
        
        if self.change_direction_timer >= self.change_direction_delay:
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.direction.length() > 0:
                self.direction = self.direction.normalize()
            self.change_direction_timer = 0
            self.change_direction_delay = random.randint(60, 180)
            
        # Move
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Keep on screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction.x *= -1
            self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction.y *= -1
            self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
        # Production
        if self.fed and not self.has_product:
            self.product_timer += dt
            if self.product_timer >= self.data["product_time"]:
                self.has_product = True
                self.product_timer = 0
                
        # Happiness decreases if not fed
        if not self.fed and self.happiness > 0:
            self.happiness -= 0.1 * dt
            
    def feed(self):
        """Feed the animal"""
        self.fed = True
        self.happiness = min(100, self.happiness + 20)
        
    def collect_product(self):
        """Collect animal product"""
        if self.has_product:
            self.has_product = False
            self.fed = False
            return self.data["product"], self.data["product_value"]
        return None, 0
        
    def draw_status(self, surface):
        """Draw status indicators above animal"""
        if self.has_product:
            # Draw exclamation mark when product ready
            pygame.draw.circle(surface, YELLOW, 
                             (self.rect.centerx, self.rect.top - 10), 4)
            pygame.draw.circle(surface, YELLOW, 
                             (self.rect.centerx, self.rect.top - 16), 2)