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
    
    @property
    def speed(self):
        return self.__speed

    @property
    def screen(self):
        return self.__screen

    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect

    @property
    def weapon(self):
        return self.__weapon

    @health.setter
    def health(self, value):
        if not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid int for health.')
        self.__health = value

    @speed.setter
    def speed(self, value):
        if not isinstance(value, int):
            raise RuntimeError('Illegal value for entity speed')
        self.__speed = value

    @screen.setter
    def screen(self, new_screen):
        if not isinstance(new_screen, pygame.Surface):
            raise RuntimeError('Screen setter failure. Non-screen passed to entity2.screen setter')
        self.__screen = new_screen

    @image.setter
    def image(self, value):
        if not isinstance(value, pygame.Surface):
            raise RuntimeError('Illegal value set for player sprite')
        self.__image = value

    @rect.setter
    def rect(self, value):
        if not isinstance(value, pygame.Rect):
            raise RuntimeError('Illegal value set to player rectangle')
        self.__rect = value

    @weapon.setter
    def weapon(self, value):
       # if not isinstance(value, weapon.Weapon):
       #     raise RuntimeError('Invalid weapon loaded onto player ship ' + value)
        self.__weapon = value

    @abstractmethod
    def move(self):
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        raise NotImplementedError