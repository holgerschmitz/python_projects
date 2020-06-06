#! /usr/bin/env python

import pygame

pygame.init()
running = 1
count = 1

screen = pygame.display.set_mode((500, 500))
screen.fill((255, 0, 0))
# s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
pygame.draw.line(screen, (0, 0, 0), (250, 250), (250 + 200, 250))
pygame.display.flip()

while running:
    count = count+1
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    print(count)