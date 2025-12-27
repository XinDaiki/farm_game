import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self,pos,text):
        super().__init__()
        self.image = pygame.Surface((28,28))
        self.image.fill((200,100,100))
        self.rect = self.image.get_rect(center=pos)
        self.text = text

    def talk(self):
        print(self.text)
