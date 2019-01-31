import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import weapon
from abc import *

class entity2(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()
        self.health = 1
        self.screen = pygame.display.get_surface()

        @property
        def health(self):
            return self.__health
        
        @health.setter
        def health(self, value):
            if not isinstance(value, int):
                raise RuntimeError(value + ' is not a valid int for health.')
            self.__health = value

        @property
        def screen(self):
            return self.__screen
        
        @screen.setter
        def screen(self, new_screen):
            if not isinstance(new_screen, pygame.surface):
                raise RuntimeError('Screen setter failure. Non-screen passed to entity2.screen setter')
            self.__screen = new_screen

    @abstractmethod
    def move(self):
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        raise NotImplementedError