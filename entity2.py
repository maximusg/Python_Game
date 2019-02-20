import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
import weapon
import math

main_dir = os.path.split(os.path.abspath(__file__))[0]

class entity2(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.health = 1
        self.screen = pygame.display.get_surface()
        self.angle = 0
        self.speed = 0
        self.speedX = 0
        self.speedY = 0
        self.acceleration = 0
       



        @property
        def health(self):
            return self.__health
        
        @health.setter
        def health(self, value):
            if not isinstance(value, int):
                raise RuntimeError(value + ' is not a valid int for health.')
            self.__health = value

        @property
        def angle(self):
            return self.__angle
        
        @angle.setter
        def angle(self, value):
            if not isinstance(value, int):
                raise RuntimeError(value + ' is not a valid int for angle.')
            self.__angle = value



