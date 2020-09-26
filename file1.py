import pygame
from pygame.draw import *
import math


pygame.init()

FPS = 30
eyebrow1 = [(189, 167), (197, 153), (128, 113), (120, 127), (189, 167)]
eyebrow2 = [(221, 150), (213, 136), (274, 101), (282, 115), (221, 150)]
screen = pygame.display.set_mode((400, 400))

screen.fill((194, 172, 171))
pygame.draw.circle(screen, (234, 255, 0), (200, 200), 100)
pygame.draw.circle(screen, (0, 0, 0), (200, 200), 100, 1)
pygame.draw.circle(screen, (255, 0, 0), (160, 170), 20)
pygame.draw.circle(screen, (255, 0, 0), (240, 170), 17)
pygame.draw.circle(screen, (0, 0, 0), (160, 170), 8)
pygame.draw.circle(screen, (0, 0, 0), (240, 170), 8)
pygame.draw.circle(screen, (0, 0, 0), (160, 170), 20, 1)
pygame.draw.circle(screen, (0, 0, 0), (240, 170), 17, 1)
pygame.draw.polygon(screen, (0, 0, 0), eyebrow1)
pygame.draw.polygon(screen, (0, 0, 0), eyebrow2)
pygame.draw.rect(screen, (255, 0, 0), (160, 250, 80, 20))

pygame.display.update()
pygame.image.save(screen, './smile.png')
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()