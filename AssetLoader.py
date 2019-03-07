import copy
import pygame
import os
from pygame.locals import RLEACCEL

DEBUG=True ##DO NOT MESS WITH ME


def load_image(name, colorkey=-1):
    MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
    '''Accepts a filename and colorkey, throws an exception if the file does not exist. Returns the pygame.image object
       as well as it's rectangle for manipulation.'''
    fullname = os.path.join(MAIN_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        raise RuntimeError('Cannot load image:' + fullname)
    if image.get_alpha(): ##not reliable
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class AssetLoader(object):
    
    __hash__ = None

    def __init__(self):
        super().__init__()
        self.assets = {}

        if DEBUG:
            self.dict_hits = 0
            self.dict_misses = 0

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        if not isinstance(value, dict):
            raise RuntimeError('AssetLoader attempting to load non-dictionary for assets.')
        self.__assets = value

    def __str__(self):
        result = 'Current Contents of AssetLoader\n'
        if DEBUG:
            result += '# of dict hits: '+str(self.dict_hits)+' | # of dict misses: '+str(self.dict_misses)+'\n'
        for item in self.assets:
            result += str(item) + '\n'
        return result

    def getAsset(self, name):
        if name in self.assets:
            if DEBUG:
                self.dict_hits += 1
            result = self.assets[name]
            newcpy = copy.deepcopy(result)
            temp_rect = newcpy[1]
            temp_img = pygame.image.frombuffer(newcpy[0], (newcpy[2], newcpy[3]), 'RGBA').convert_alpha()
            return (temp_img, temp_rect)
        else:
            if DEBUG:
                self.dict_misses += 1
            self.__loadAsset(name)
            result = self.assets[name]
            newcpy = copy.deepcopy(result)
            temp_rect = newcpy[1]
            temp_img = pygame.image.frombuffer(newcpy[0], (newcpy[2], newcpy[3]), 'RGBA').convert_alpha()
            return (temp_img, temp_rect)

    def __loadAsset(self, name):
        image, rect = load_image(name)
        image_buffer = pygame.image.tostring(image, 'RGBA')
        self.assets[name] = (image_buffer, rect, rect.width, rect.height)