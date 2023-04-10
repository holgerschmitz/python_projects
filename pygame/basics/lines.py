#!python3

import pygame

pygame.init()
running = True
xvel = 1
yvel = 0

xpos = 25
ypos = 25

screen = pygame.display.set_mode((500, 500))

MOVEEVENT = pygame.USEREVENT+1
pygame.time.set_timer(MOVEEVENT, 120)

while running:

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        print('Quitting!')
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            xvel = 1
            yvel = 0
        elif event.key == pygame.K_LEFT:
            xvel = -1
            yvel = 0
        elif event.key == pygame.K_UP:
            xvel = 0
            yvel = -1
        elif event.key == pygame.K_DOWN:
            xvel = 0
            yvel = 1
    elif event.type == MOVEEVENT:
        xpos = xpos + xvel
        ypos = ypos + yvel

    screen.fill((255, 0, 0))


    xcoord = 10*xpos
    ycoord = 10*ypos

    pygame.draw.rect(screen, (0, 0, 0), (xcoord, ycoord, 10, 10))
    pygame.display.flip()
    print(f"{xpos}, {ypos}")