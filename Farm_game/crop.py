import pygame
import time
from settings import TILE_SIZE

class Crop(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.stage = 0

        # load crop growth stages
        self.images = [
            pygame.image.load("assets/crop.png").convert_alpha(),
          # pygame.image.load("assets/crop_stage2.png").convert_alpha(),
           # pygame.image.load("assets/crop_stage3.png").convert_alpha()
        ]

        self.image = self.images[self.stage]
        self.rect = self.image.get_rect(topleft=pos)

        self.start_time = time.time()

    def update(self):
        if time.time() - self.start_time > 4 and self.stage < 2:
            self.stage += 1
            self.image = self.images[self.stage]
            self.start_time = time.time()
