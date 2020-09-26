import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
# lightclouds = [rect1, rect2, ...] список данных о светлых облаках, которые надо нарисовать
# darklouds = [rect1, ...] аналогично со светлыми облаками
lightclouds = [(-600, 20, 1000, 200), (500, -25, 600, 120), (350, 130, 700, 140),
               (250, 300, 700, 150), (-150, 250, 680, 150)]
greyclouds = [(120, 80, 760, 120), (-333, 200, 666, 160), (169, 380, 666, 150)]
screen = pygame.display.set_mode((794, 1123))

pygame.draw.rect(screen, (0, 34, 43), (0, 0, 794, 579))
pygame.draw.rect(screen, (34,43,0), (0, 579, 794, 1123))
pygame.draw.circle(screen, (242, 242, 242), (510, 265), 120)

for cloud in lightclouds:
    pygame.draw.ellipse(screen, (102, 102, 102), cloud)
for cloud in greyclouds:
    pygame.draw.ellipse(screen, (51, 51, 51), cloud)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
