import pygame
import random
from settings import *

class Animal(pygame.sprite.Sprite):
    ANIMAL_TYPES = {
        "chicken": {
            "color": (255, 255, 255),
            "size": (20, 18),
            "product": "egg",
            "product_time": 180,  # 3 minutes (180 seconds)
            "product_value": 15,
            "speed": 1.2,
            "wander_radius": 100,
            "feed_cooldown": 180
        },
        "cow": {
            "color": (139, 90, 43),
            "size": (28, 24),
            "product": "milk",
            "product_time": 240,  # 4 minutes (240 seconds)
            "product_value": 20,
            "speed": 0.8,
            "wander_radius": 80,
            "feed_cooldown": 180
        },
        "sheep": {
            "color": (245, 245, 245),
            "size": (24, 20),
            "product": "wool",
            "product_time": 210,  # 3.5 minutes (210 seconds)
            "product_value": 25,
            "speed": 1.0,
            "wander_radius": 90,
            "feed_cooldown": 180
        },
        "pig": {
            "color": (255, 192, 203),
            "size": (26, 22),
            "product": "truffle",
            "product_time": 300,  # 5 minutes (300 seconds)
            "product_value": 30,
            "speed": 0.9,
            "wander_radius": 85,
            "feed_cooldown": 180
        },
        "goat": {
            "color": (210, 180, 140),
            "size": (24, 22),
            "product": "cheese",
            "product_time": 270,  # 4.5 minutes (270 seconds)
            "product_value": 35,
            "speed": 1.1,
            "wander_radius": 95,
            "feed_cooldown": 180
        },
        "duck": {
            "color": (255, 255, 100),
            "size": (18, 16),
            "product": "duck_egg",
            "product_time": 195,  # 3.25 minutes (195 seconds)
            "product_value": 28,
            "speed": 1.3,
            "wander_radius": 110,
            "feed_cooldown": 180
        },
        "rabbit": {
            "color": (200, 200, 200),
            "size": (16, 14),
            "product": "rabbit_foot",
            "product_time": 180,  # 3 minutes (180 seconds)
            "product_value": 35,
            "speed": 1.5,
            "wander_radius": 120,
            "feed_cooldown": 180
        },
        "horse": {
            "color": (101, 67, 33),
            "size": (32, 28),
            "product": "horseshoe",
            "product_time": 300,  # 5 minutes (300 seconds)
            "product_value": 60,
            "speed": 0.7,
            "wander_radius": 70,
            "feed_cooldown": 180
        },
        "llama": {
            "color": (220, 200, 180),
            "size": (26, 30),
            "product": "llama_wool",
            "product_time": 255,  # 4.25 minutes (255 seconds)
            "product_value": 45,
            "speed": 0.85,
            "wander_radius": 80,
            "feed_cooldown": 180
        },
        "turkey": {
            "color": (160, 82, 45),
            "size": (22, 20),
            "product": "turkey_feather",
            "product_time": 225,  # 3.75 minutes (225 seconds)
            "product_value": 32,
            "speed": 1.0,
            "wander_radius": 100,
            "feed_cooldown": 180
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
        
        # Store home position for wandering
        self.home_pos = pygame.math.Vector2(pos)
        self.position = pygame.math.Vector2(pos)
        
        # Movement behavior
        self.speed = self.data["speed"]
        self.base_speed = self.speed
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        
        # Behavior timers
        self.change_direction_timer = 0
        self.change_direction_delay = random.randint(60, 180)
        self.pause_timer = 0
        self.is_paused = random.choice([True, False])
        self.pause_duration = random.randint(30, 120) if self.is_paused else 0
        
        # Movement state
        self.wander_radius = self.data["wander_radius"]
        self.movement_state = random.choice(["wander", "pause", "roam"])
        self.state_timer = random.randint(120, 300)
        
        # Animal state system
        self.state = "has_product"
        self.product_timer = 0
        self.feed_cooldown_timer = 0
        self.feed_cooldown_duration = self.data["feed_cooldown"]
        
        # Legacy support
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
        
        elif self.animal_type == "pig":
            # Body
            pygame.draw.ellipse(self.image, color, (3, 8, 20, 14))
            # Head
            pygame.draw.circle(self.image, color, (20, 12), 6)
            # Snout
            pygame.draw.ellipse(self.image, (255, 182, 193), (21, 11, 4, 3))
            # Eye
            pygame.draw.circle(self.image, BLACK, (20, 10), 1)
            # Ear
            pygame.draw.polygon(self.image, color, [(18, 8), (16, 6), (18, 6)])
            # Tail (curly)
            pygame.draw.arc(self.image, color, (1, 10, 6, 6), 0, 3.14, 2)
            # Legs
            for x in [7, 11, 15, 19]:
                pygame.draw.line(self.image, color, (x, 22), (x, 20), 2)
        
        elif self.animal_type == "goat":
            # Body
            pygame.draw.ellipse(self.image, color, (2, 8, 20, 12))
            # Head
            pygame.draw.circle(self.image, color, (18, 10), 5)
            # Horns
            pygame.draw.line(self.image, (139, 69, 19), (16, 8), (14, 4), 2)
            pygame.draw.line(self.image, (139, 69, 19), (20, 8), (22, 4), 2)
            # Eye
            pygame.draw.circle(self.image, BLACK, (18, 9), 1)
            # Beard
            pygame.draw.line(self.image, (100, 80, 60), (18, 13), (18, 16), 2)
            # Legs
            for x in [6, 10, 14, 18]:
                pygame.draw.line(self.image, color, (x, 20), (x, 18), 2)
        
        elif self.animal_type == "duck":
            # Body
            pygame.draw.ellipse(self.image, color, (2, 6, 14, 10))
            # Head
            pygame.draw.circle(self.image, color, (13, 5), 4)
            # Bill
            pygame.draw.polygon(self.image, (255, 165, 0), 
                              [(15, 5), (18, 4), (18, 6)])
            # Eye
            pygame.draw.circle(self.image, BLACK, (13, 4), 1)
            # Wing
            pygame.draw.ellipse(self.image, (200, 200, 50), (4, 8, 8, 5))
            # Legs (webbed)
            pygame.draw.line(self.image, (255, 165, 0), (6, 16), (6, 14), 2)
            pygame.draw.line(self.image, (255, 165, 0), (10, 16), (10, 14), 2)
        
        elif self.animal_type == "rabbit":
            # Body
            pygame.draw.ellipse(self.image, color, (2, 6, 12, 8))
            # Head
            pygame.draw.circle(self.image, color, (11, 6), 4)
            # Long ears
            pygame.draw.ellipse(self.image, color, (9, 0, 3, 6))
            pygame.draw.ellipse(self.image, color, (13, 0, 3, 6))
            # Eye
            pygame.draw.circle(self.image, BLACK, (11, 5), 1)
            # Nose
            pygame.draw.circle(self.image, (255, 192, 203), (11, 7), 1)
            # Cotton tail
            pygame.draw.circle(self.image, WHITE, (3, 10), 2)
        
        elif self.animal_type == "horse":
            # Body
            pygame.draw.ellipse(self.image, color, (4, 10, 24, 16))
            # Neck
            pygame.draw.rect(self.image, color, (22, 6, 6, 10))
            # Head
            pygame.draw.ellipse(self.image, color, (24, 4, 8, 8))
            # Mane
            pygame.draw.polygon(self.image, (50, 30, 20), 
                              [(24, 6), (26, 4), (28, 6)])
            # Eye
            pygame.draw.circle(self.image, BLACK, (28, 7), 1)
            # Legs
            for x in [8, 12, 18, 22]:
                pygame.draw.line(self.image, color, (x, 26), (x, 24), 3)
        
        elif self.animal_type == "llama":
            # Body
            pygame.draw.ellipse(self.image, color, (3, 14, 20, 12))
            # Long neck
            pygame.draw.rect(self.image, color, (18, 6, 5, 12))
            # Head
            pygame.draw.ellipse(self.image, color, (18, 4, 8, 8))
            # Ears (upright)
            pygame.draw.polygon(self.image, color, [(20, 4), (19, 2), (21, 2)])
            pygame.draw.polygon(self.image, color, [(24, 4), (23, 2), (25, 2)])
            # Eye
            pygame.draw.circle(self.image, BLACK, (21, 6), 1)
            # Fluffy top
            pygame.draw.circle(self.image, (240, 220, 200), (13, 12), 6)
            # Legs
            for x in [7, 11, 15, 19]:
                pygame.draw.line(self.image, color, (x, 26), (x, 24), 2)
        
        elif self.animal_type == "turkey":
            # Body
            pygame.draw.ellipse(self.image, color, (3, 8, 16, 12))
            # Head/Neck
            pygame.draw.line(self.image, color, (15, 12), (18, 8), 3)
            pygame.draw.circle(self.image, (200, 100, 100), (18, 7), 3)
            # Eye
            pygame.draw.circle(self.image, BLACK, (18, 6), 1)
            # Wattle (red thing)
            pygame.draw.circle(self.image, RED, (18, 9), 2)
            # Tail fan
            for i in range(5):
                angle_offset = (i - 2) * 0.3
                x = int(5 + 6 * (1 - abs(i - 2) * 0.2))
                pygame.draw.circle(self.image, (100, 60, 30), (x, 10), 3)
            # Legs
            pygame.draw.line(self.image, (255, 165, 0), (9, 20), (9, 18), 2)
            pygame.draw.line(self.image, (255, 165, 0), (13, 20), (13, 18), 2)
    
    def choose_new_direction(self):
        """Choose a new random direction"""
        distance_from_home = self.position.distance_to(self.home_pos)
            
        if distance_from_home > self.wander_radius * 1.5:
            direction_to_home = self.home_pos - self.position
            if direction_to_home.length() > 0:
                self.direction = direction_to_home.normalize()
                self.direction.x += random.uniform(-0.3, 0.3)
                self.direction.y += random.uniform(-0.3, 0.3)
                if self.direction.length() > 0:
                    self.direction = self.direction.normalize()
        else:
            self.direction = pygame.math.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
            if self.direction.length() > 0:
                self.direction = self.direction.normalize()
    
    def change_movement_state(self):
        """Change between different movement behaviors"""
        states = ["wander", "pause", "roam", "wander", "roam"]
        self.movement_state = random.choice(states)
        
        if self.movement_state == "pause":
            self.is_paused = True
            self.pause_duration = random.randint(30, 120)
            self.pause_timer = 0
            self.speed = 0
        elif self.movement_state == "wander":
            self.is_paused = False
            self.speed = self.base_speed * random.uniform(0.5, 1.0)
            self.choose_new_direction()
        else:
            self.is_paused = False
            self.speed = self.base_speed * random.uniform(0.7, 1.3)
            self.choose_new_direction()
        
        self.state_timer = random.randint(120, 300)
                
    def update(self, dt):
        """Update animal behavior"""
        # State management
        self.state_timer -= 1
        if self.state_timer <= 0:
            self.change_movement_state()
        
        # Animal state machine
        if self.state == "cooldown":
            self.feed_cooldown_timer -= 1
            if self.feed_cooldown_timer <= 0:
                self.state = "producing"
                self.product_timer = 0
                
        elif self.state == "producing":
            self.product_timer += dt
            if self.product_timer >= self.data["product_time"]:
                self.state = "has_product"
                self.product_timer = 0
                self.is_paused = True
                self.pause_duration = 30
                self.pause_timer = 0
        
        # Handle pausing
        if self.is_paused:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_duration:
                self.is_paused = False
                self.speed = self.base_speed * random.uniform(0.7, 1.2)
                self.choose_new_direction()
        else:
            # Random movement direction changes
            self.change_direction_timer += 1
            
            if self.change_direction_timer >= self.change_direction_delay:
                self.choose_new_direction()
                self.change_direction_timer = 0
                self.change_direction_delay = random.randint(60, 180)
                
                if random.random() < 0.2:
                    self.is_paused = True
                    self.pause_duration = random.randint(20, 60)
                    self.pause_timer = 0
                    self.speed = 0
            
            # Move using float position
            self.position.x += self.direction.x * self.speed
            self.position.y += self.direction.y * self.speed
            
            # Update rect position
            self.rect.centerx = int(self.position.x)
            self.rect.centery = int(self.position.y)
            
            # Keep on screen with bouncing
            if self.rect.left < 0:
                self.position.x = self.rect.width // 2
                self.direction.x = abs(self.direction.x)
            elif self.rect.right > SCREEN_WIDTH:
                self.position.x = SCREEN_WIDTH - self.rect.width // 2
                self.direction.x = -abs(self.direction.x)
                
            if self.rect.top < 0:
                self.position.y = self.rect.height // 2
                self.direction.y = abs(self.direction.y)
            elif self.rect.bottom > SCREEN_HEIGHT:
                self.position.y = SCREEN_HEIGHT - self.rect.height // 2
                self.direction.y = -abs(self.direction.y)
            
            if (self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH or 
                self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT):
                if random.random() < 0.5:
                    self.choose_new_direction()
            
    def feed(self):
        """Feed the animal"""
        if self.state == "needs_feed":
            self.state = "cooldown"
            self.feed_cooldown_timer = self.feed_cooldown_duration
            self.happiness = min(100, self.happiness + 20)
            self.is_paused = True
            self.pause_duration = 20
            self.pause_timer = 0
            return True
        return False
        
    def collect_product(self):
        """Collect animal product"""
        if self.state == "has_product":
            self.state = "needs_feed"
            return self.data["product"], self.data["product_value"]
        return None, 0
    
    def can_collect(self):
        """Check if product can be collected"""
        return self.state == "has_product"
    
    def can_feed(self):
        """Check if animal can be fed"""
        return self.state == "needs_feed"
    
    def get_state_info(self):
        """Get human-readable state information"""
        if self.state == "has_product":
            return "Ready to collect!"
        elif self.state == "needs_feed":
            return "Hungry - needs feeding"
        elif self.state == "cooldown":
            time_left = int(self.feed_cooldown_timer / 120)
            return f"Digesting... ({time_left}s)"
        elif self.state == "producing":
            progress = int((self.product_timer / self.data["product_time"]) * 100)
            return f"Producing... ({progress}%)"
        return ""
        
    def draw_status(self, surface):
        """Draw status indicators above animal"""
        if self.state == "has_product":
            pygame.draw.circle(surface, YELLOW, 
                             (self.rect.centerx, self.rect.top - 10), 4)
            pygame.draw.circle(surface, YELLOW, 
                             (self.rect.centerx, self.rect.top - 16), 2)
                             
        elif self.state == "needs_feed":
            heart_x = self.rect.centerx
            heart_y = self.rect.top - 12
            pygame.draw.circle(surface, RED, (heart_x - 3, heart_y), 3)
            pygame.draw.circle(surface, RED, (heart_x + 3, heart_y), 3)
            pygame.draw.polygon(surface, RED, [
                (heart_x - 6, heart_y),
                (heart_x, heart_y + 6),
                (heart_x + 6, heart_y)
            ])
            
        elif self.state == "cooldown":
            clock_x = self.rect.centerx
            clock_y = self.rect.top - 12
            pygame.draw.circle(surface, GRAY, (clock_x, clock_y), 4)
            pygame.draw.circle(surface, WHITE, (clock_x, clock_y), 4, 1)
            pygame.draw.line(surface, WHITE, (clock_x, clock_y), (clock_x, clock_y - 3), 1)
            
        elif self.state == "producing":
            pygame.draw.circle(surface, (100, 200, 100), 
                             (self.rect.centerx, self.rect.top - 10), 3)
