import copy
import pygame
import os
import array
from pygame.locals import RLEACCEL

class AssetLoader(object):
    '''A structure meant to assist with constant loading/reloading of sprites. Allows any sprite class to query for a given filename,
       and if that file has been accessed before, it serves it up without having to go to the disk again. So while any given level may have thousands
       of sprites (especially if you're trigger happy) each sprite type (player, enemy, bullet, etc) is only incurring the cost of a single trip to the
       disk.'''

    __hash__ = None ##This will disable some builtin functions that don't apply, nor do we want them to apply.

    def __init__(self):
        super().__init__()
        self.assets = {}

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        if not isinstance(value, dict):
            raise RuntimeError('AssetLoader attempting to load non-dictionary for assets.')
        self.__assets = value

    def getAsset(self, name):
        '''Accepts an OS path or path-like string, returns that filename's sprite surface and rectangle.'''

        if name in self.assets:
            
            result = self.assets[name]
            image = pygame.surfarray.make_surface(result)
            
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
            image = image.convert_alpha()
            return image, image.get_rect()

        else:
            return self.__loadAsset(name)

    def __loadAsset(self, name):
        '''The user should not be calling this function directly. Use getAsset(name)'''
        try:
            image = pygame.image.load(str(name))
        except pygame.error:
            raise RuntimeError('Cannot load image:' + name)

        self.assets[name] = pygame.surfarray.array3d(image)

        if image.get_alpha():
            image = image.convert_alpha()
        else:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
            image = image.convert_alpha()
        return image, image.get_rect()
