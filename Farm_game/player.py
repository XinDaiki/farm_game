import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Create player sprite (simple character design)
        self.image = pygame.Surface((28, 32))
        self.image.fill((255, 200, 150))  # Skin color
        pygame.draw.rect(self.image, (100, 50, 200), (6, 8, 16, 12))  # Shirt
        pygame.draw.rect(self.image, (50, 50, 150), (6, 20, 16, 12))  # Pants
        pygame.draw.circle(self.image, (255, 220, 177), (14, 6), 6)  # Head
        pygame.draw.circle(self.image, BLACK, (11, 5), 2)  # Left eye
        pygame.draw.circle(self.image, BLACK, (17, 5), 2)  # Right eye
        
        self.rect = self.image.get_rect(center=pos)
        self.speed = 3
        self.money = INITIAL_MONEY
        self.energy = 100
        self.max_energy = 100
        
        # Tool system
        self.current_tool = "hand"  # hand, hoe, watering_can, axe
        self.tool_range = 40
        
    def update(self, keys, dt):
        # Movement
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Energy regeneration
        if self.energy < self.max_energy:
            self.energy += 0.1 * dt
            
    def use_energy(self, amount):
        """Use energy and return True if successful"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
        
    def change_tool(self):
        """Cycle through tools"""
        tools = ["hand", "hoe", "watering_can", "axe", "scythe"]
        current_index = tools.index(self.current_tool)
        self.current_tool = tools[(current_index + 1) % len(tools)]
        
    def get_tool_position(self):
        """Get position where tool is being used"""
        return self.rect.center