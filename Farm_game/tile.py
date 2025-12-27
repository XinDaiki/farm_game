import pygame
from settings import TILE_SIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, kind):
        super().__init__()

        if kind == "G":
            self.image = pygame.image.load("assets/grass.png").convert_alpha()
        elif kind == "S":
            self.image = pygame.image.load("assets/soil.png").convert_alpha()
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect(topleft=pos)
