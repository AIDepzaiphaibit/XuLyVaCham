import pygame, sys, math
from pygame.locals import *

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((400, 400))

def circleCollision(center1, radius1, center2, radius2):
    d = math.sqrt((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)
    if d <= radius1 + radius2:
        return True
    return False

center1 = [0, 0]
radius1 = 20
center2 = [200, 200]
radius2 = 30

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill((0, 0, 0))

    center1[0], center1[1] = pygame.mouse.get_pos()

    pygame.draw.circle(DISPLAYSURF, (255, 255, 0), center2, radius2)
    if circleCollision(center1, radius1, center2, radius2) == True:
        pygame.draw.circle(DISPLAYSURF, (255, 0, 0), center1, radius1)
    else:
        pygame.draw.circle(DISPLAYSURF, (0, 255, 0), center1, radius1)

    pygame.display.update()
    fpsClock.tick(FPS)