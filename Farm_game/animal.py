import pygame, random

class Animal(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((24,24))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.x += random.choice([-1,0,1])
        self.rect.y += random.choice([-1,0,1])
