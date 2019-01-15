""" GUI is used for all visual opeartions for the game.
Displays the screen, maps skins/graphics to locations on screen"""

import sys
import pygame

pygame.init()

WINDOWSIZE = (800, 600)

SCREEN = pygame.display.set_mode(WINDOWSIZE)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
