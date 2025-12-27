import pygame, json, sys
from settings import *
from player import Player
from inventory import Inventory
from crafting import Crafting
from world import World
from animal import Animal
from npc import NPC
from time_system import TimeSystem

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = Player((400,300))
players = pygame.sprite.Group(player)

world = World()
world.load("farm_game/map.txt")

animals = pygame.sprite.Group(Animal((200,200)))
npc = NPC((500,300),"Hello farmer!")

inv = Inventory()
craft = Crafting()
time_sys = TimeSystem()
font = pygame.font.SysFont(None,24)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if inv.use("seed"):
                world.plant(pygame.mouse.get_pos())

    players.update()
    animals.update()
    world.crops.update()
    time_sys.update()

    screen.fill((0,0,0))
    world.tiles.draw(screen)
    world.crops.draw(screen)
    animals.draw(screen)
    players.draw(screen)

    if time_sys.time >= 18:
        dark = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        dark.set_alpha(120)
        dark.fill((0,0,40))
        screen.blit(dark,(0,0))

    ui = font.render(f"Day {time_sys.day}  Time {int(time_sys.time)}",True,(255,255,255))
    screen.blit(ui,(10,10))

    pygame.display.flip()
    clock.tick(FPS)
