import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # load player sprite
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.speed = 4

    def update(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_w]:
            self.rect.y -= self.speed
        if k[pygame.K_s]:
            self.rect.y += self.speed
        if k[pygame.K_a]:
            self.rect.x -= self.speed
        if k[pygame.K_d]:
            self.rect.x += self.speed
