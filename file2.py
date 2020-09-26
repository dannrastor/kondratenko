import pygame
from pygame.draw import *
import math


pygame.init()

FPS = 30
screen = pygame.display.set_mode((794, 1123))

pygame.draw.rect(screen, (0, 34, 43), (0, 0, 794, 579))
pygame.draw.rect(screen, (34,43,0), (0, 579, 794, 1123))
pygame.draw.circle(screen, (242, 242, 242), (510, 265), 120)
pygame.display.update()

clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
