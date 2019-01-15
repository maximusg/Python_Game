import pygame, sys

pygame.init()

windowSize =(800,600)

screen = pygame.display.set_mode(windowSize)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    pygame.display.update()