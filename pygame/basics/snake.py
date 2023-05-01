#!python3

import pygame
import random

pygame.init()
running = True
xvel = 1
yvel = 0

xpos = 25
ypos = 25

screen = pygame.display.set_mode((500, 500))

MOVEEVENT = pygame.USEREVENT+1
FOODEVENT = pygame.USEREVENT+2
pygame.time.set_timer(MOVEEVENT, 120)
pygame.time.set_timer(FOODEVENT, 1000)

# area = []
# for i in range(100):
#     row = []
#     for j in range(100):
#         row.append['']
#     area.append(row)

haveFood = False
foodPos = None

tail = []

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
        if haveFood and xpos==foodPos[0] and ypos==foodPos[1]:
            haveFood = False
            tail.insert(0, [0,0])

        tail.append([xpos, ypos])
        tail.pop(0)
        xpos = xpos + xvel
        ypos = ypos + yvel
    elif event.type == FOODEVENT:
        if not haveFood:
            foodPos = [random.randrange(50), random.randrange(50)]
            haveFood = True

    screen.fill((255, 255, 255))


    xcoord = 10*xpos
    ycoord = 10*ypos

    if haveFood:
        pygame.draw.rect(screen, (255, 0, 0), (foodPos[0]*10, foodPos[1]*10, 10, 10))

    for tailPos in tail:
        pygame.draw.rect(screen, (80, 80, 80), (tailPos[0]*10, tailPos[1]*10, 10, 10))

    pygame.draw.rect(screen, (0, 0, 0), (xcoord, ycoord, 10, 10))
    pygame.display.flip()
    print(f"{xpos}, {ypos}")