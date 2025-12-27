import pygame
from tile import Tile
from crop import Crop
from settings import TILE_SIZE

class World:
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.crops = pygame.sprite.Group()

    def load(self, file):
        with open(file) as f:
            for y, row in enumerate(f):
                for x, t in enumerate(row.strip()):
                    self.tiles.add(
                        Tile((x * TILE_SIZE, y * TILE_SIZE), t)
                    )

    def plant(self, pos):
        x = pos[0] // TILE_SIZE * TILE_SIZE
        y = pos[1] // TILE_SIZE * TILE_SIZE
        self.crops.add(Crop((x, y)))
