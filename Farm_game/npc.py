import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
    NPC_DATA = {
        "shopkeeper": {
            "color": (150, 75, 0),
            "dialogues": [
                "Welcome to my shop!",
                "Need some seeds?",
                "Fresh supplies daily!",
                "How's the farm going?"
            ],
            "shop": True
        },
        "mayor": {
            "color": (50, 50, 150),
            "dialogues": [
                "Welcome to our village!",
                "The harvest festival is coming!",
                "Keep up the good work!",
                "We're proud of our farmers!"
            ],
            "shop": False
        },
        "fisherman": {
            "color": (100, 150, 200),
            "dialogues": [
                "The fish are biting today!",
                "Have you tried fishing?",
                "I caught a big one yesterday!",
                "The lake is beautiful this time of year."
            ],
            "shop": False
        }
    }
    
    def __init__(self, pos, npc_type="shopkeeper"):
        super().__init__()
        
        self.npc_type = npc_type
        self.data = self.NPC_DATA[npc_type]
        
        # Create NPC sprite
        self.image = pygame.Surface((28, 32))
        self.create_sprite()
        
        self.rect = self.image.get_rect(center=pos)
        
        # Dialogue
        self.current_dialogue = 0
        self.dialogue_visible = False
        self.dialogue_timer = 0
        self.font = pygame.font.Font(None, 18)
        
    def create_sprite(self):
        """Create NPC visual representation"""
        color = self.data["color"]
        
        # Body
        self.image.fill((255, 200, 150))  # Skin
        pygame.draw.rect(self.image, color, (6, 8, 16, 12))  # Shirt
        pygame.draw.rect(self.image, (50, 50, 50), (6, 20, 16, 12))  # Pants
        
        # Head
        pygame.draw.circle(self.image, (255, 220, 177), (14, 6), 6)
        pygame.draw.circle(self.image, BLACK, (11, 5), 2)  # Left eye
        pygame.draw.circle(self.image, BLACK, (17, 5), 2)  # Right eye
        pygame.draw.line(self.image, BLACK, (12, 8), (16, 8), 1)  # Smile
        
        # Hat (for shopkeeper)
        if self.npc_type == "shopkeeper":
            pygame.draw.rect(self.image, color, (8, 0, 12, 4))
            pygame.draw.rect(self.image, color, (6, 3, 16, 2))
            
        # Fishing rod (for fisherman)
        if self.npc_type == "fisherman":
            pygame.draw.line(self.image, BROWN, (24, 12), (28, 2), 2)
            
    def talk(self):
        """Start dialogue with NPC"""
        self.dialogue_visible = True
        self.dialogue_timer = 180  # Show for 3 seconds at 60 FPS
        dialogue = self.data["dialogues"][self.current_dialogue]
        self.current_dialogue = (self.current_dialogue + 1) % len(self.data["dialogues"])
        return dialogue
        
    def update(self, dt):
        """Update NPC"""
        if self.dialogue_visible:
            self.dialogue_timer -= 1
            if self.dialogue_timer <= 0:
                self.dialogue_visible = False
                
    def draw_dialogue(self, surface):
        """Draw dialogue bubble"""
        if self.dialogue_visible:
            dialogue = self.data["dialogues"][self.current_dialogue - 1]
            
            # Create dialogue box
            padding = 10
            text_surface = self.font.render(dialogue, True, BLACK)
            box_width = text_surface.get_width() + padding * 2
            box_height = text_surface.get_height() + padding * 2
            
            # Position above NPC
            box_x = self.rect.centerx - box_width // 2
            box_y = self.rect.top - box_height - 10
            
            # Keep on screen
            box_x = max(5, min(box_x, SCREEN_WIDTH - box_width - 5))
            box_y = max(5, box_y)
            
            # Draw box
            pygame.draw.rect(surface, WHITE, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, BLACK, (box_x, box_y, box_width, box_height), 2)
            
            # Draw pointer
            points = [
                (self.rect.centerx, self.rect.top - 5),
                (self.rect.centerx - 5, box_y + box_height),
                (self.rect.centerx + 5, box_y + box_height)
            ]
            pygame.draw.polygon(surface, WHITE, points)
            pygame.draw.lines(surface, BLACK, True, points, 2)
            
            # Draw text
            surface.blit(text_surface, (box_x + padding, box_y + padding))
            
    def draw_label(self, surface):
        """Draw name label above NPC"""
        if self.npc_type == "shopkeeper":
            label_font = pygame.font.Font(None, 16)
            label = label_font.render("SHOP", True, (255, 215, 0))
            label_bg = pygame.Surface((label.get_width() + 6, label.get_height() + 4))
            label_bg.fill((0, 0, 0))
            label_bg.set_alpha(180)
            
            label_x = self.rect.centerx - label.get_width() // 2 - 3
            label_y = self.rect.top - 20
            
            surface.blit(label_bg, (label_x, label_y))
            surface.blit(label, (label_x + 3, label_y + 2))
            
    def open_shop(self):
        """Return shop inventory if this NPC has a shop"""
        if self.data["shop"]:
            return {
                "wheat_seed": 10,
                "carrot_seed": 15,
                "tomato_seed": 20,
                "corn_seed": 25,
            }
        return None
