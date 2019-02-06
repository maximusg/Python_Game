import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
import weapon

main_dir = os.path.split(os.path.abspath(__file__))[0]

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


    def load_image(self, name, colorkey=None):
        fullname = os.path.join(main_dir, name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    
    def something(self):
        pass