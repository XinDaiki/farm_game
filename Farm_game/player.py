import pygame
import os
from settings import *

def import_sheet(path, frame_width, frame_height, scale=2):
    """Slices and resizes frames from the sprite sheet."""
    try:
        surface = pygame.image.load(path).convert_alpha()
    except pygame.error:
        print(f"Error: Could not find {path}")
        return None

    directions = {0: 'down', 1: 'up', 2: 'right'}
    animation_data = {'down': [], 'up': [], 'right': [], 'left': []}

    for row in range(3):
        for col in range(surface.get_width() // frame_width):
            x = col * frame_width
            y = row * frame_height
            
            frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surf.blit(surface, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
            
            # Scale up for visibility (64x64)
            scaled_size = (frame_width * scale, frame_height * scale)
            frame_surf = pygame.transform.scale(frame_surf, scaled_size)
            
            dir_name = directions[row]
            animation_data[dir_name].append(frame_surf)
            
            if dir_name == 'right':
                left_frame = pygame.transform.flip(frame_surf, True, False)
                animation_data['left'].append(left_frame)
                
    return animation_data

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        asset_folder = "assets\Character"
        
        # Load both animation sets
        self.idle_frames = import_sheet(os.path.join(asset_folder, 'Idle.png'), 32, 32, 2)
        self.walk_frames = import_sheet(os.path.join(asset_folder, 'Walk.png'), 32, 32, 2)
        
        # State and Direction
        self.status = 'idle'
        self.facing = 'down'
        self.frame_index = 0
        self.animation_speed = 10  # Increased speed for better walking feel
        
        # Image and Rect
        self.image = self.idle_frames[self.facing][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-20, -20)
        
        # Attributes (Restored for UI compatibility)
        self.speed = 3
        self.current_tool = "hand"
        self.money = INITIAL_MONEY
        self.energy = 100 
        self.max_energy = 100

    def animate(self, dt):
        # Determine which sheet to use
        if self.status == 'walk':
            current_animation = self.walk_frames[self.facing]
        else:
            current_animation = self.idle_frames[self.facing]
        
        # Cycle frames
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            
        # Update current image
        self.image = current_animation[int(self.frame_index)]

    def update(self, keys, dt):
        dx, dy = 0, 0
        
        # Movement and Facing logic
        if keys[pygame.K_w] or keys[pygame.K_UP]: 
            dy -= self.speed
            self.facing = 'up'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: 
            dy += self.speed
            self.facing = 'down'
            
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            dx -= self.speed
            self.facing = 'left'
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            dx += self.speed
            self.facing = 'right'
            
        # Update status: MUST be walk if dx or dy is not 0
        if dx != 0 or dy != 0:
            self.status = 'walk'
        else:
            self.status = 'idle'
            
        # Apply movement
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
            
        self.rect.x += dx
        self.rect.y += dy
        self.hitbox.center = self.rect.center

        # Animate!
        self.animate(dt)
        
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Energy regeneration
        if self.energy < self.max_energy:
            self.energy += 0.03 * dt


    # Helper methods for your UI and mechanics
    def use_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

    def change_tool(self):
        tools = ["hand", "hoe", "watering_can", "axe", "scythe"]
        current_index = tools.index(self.current_tool)
        self.current_tool = tools[(current_index + 1) % len(tools)]

    def get_tool_position(self):
        return self.rect.center
