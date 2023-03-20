#!python3

import pygame

pygame.init()
running = True
count = 1

screen = pygame.display.set_mode((500, 500))

while running:
    count = (count+1) % 500

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        print('Quitting!')
        running = False
    screen.fill((255, 0, 0))
    pygame.draw.line(screen, (0, 0, 0), (250, count), (250 + 200, count))
    pygame.display.flip()
    print(count)