import copy
import pygame
import os
import array
from pygame.locals import RLEACCEL

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
    '''A structure meant to assist with constant loading/reloading of sprites. Allows any sprite class to query for a given filename,
       and if that file has been accessed before, it serves it up without having to go to the disk again. So while any given level may have thousands
       of sprites (especially if you're trigger happy) each sprite type (player, enemy, bullet, etc) is only incurring the cost of a single trip to the
       disk.'''

    __hash__ = None ##This will disable some builtin functions that don't apply, nor do we want them to apply.

    def __init__(self):
        super().__init__()
        self.assets = {}

        # if DEBUG:
        #     self.dict_hits = 0
        #     self.dict_misses = 0

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        if not isinstance(value, dict):
            raise RuntimeError('AssetLoader attempting to load non-dictionary for assets.')
        self.__assets = value

    # def __str__(self):
    #     result = 'Current Contents of AssetLoader\n'
    #     if DEBUG:
    #         result += '# of dict hits: '+str(self.dict_hits)+' | # of dict misses: '+str(self.dict_misses)+'\n'
    #     for item in self.assets:
    #         result += str(item) + '\n'
    #     return result

    def getAsset(self, name):
        '''Accepts an OS path or path-like string, returns that filename's sprite surface and rectangle.'''

        if name in self.assets:
            
            # if DEBUG:
            #     self.dict_hits += 1
            result = self.assets[name]
            image = pygame.surfarray.make_surface(result)
            
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
            image = image.convert_alpha()
            return image, image.get_rect()

            # newcpy = copy.deepcopy(result) ##requires a unique copy, otherwise hilarity will ensue (this has been tested).
            # temp_rect = newcpy[1]
            # temp_img = pygame.image.frombuffer(newcpy[0], (newcpy[2], newcpy[3]), 'RGBA').convert_alpha()
            # return (temp_img, temp_rect)
        else:
            # if DEBUG:
            #     self.dict_misses += 1
            return self.__loadAsset(name)

            # result = self.assets[name]
            # newcpy = copy.deepcopy(result)
            # temp_rect = newcpy[1]
            # temp_img = pygame.image.frombuffer(newcpy[0], (newcpy[2], newcpy[3]), 'RGBA').convert_alpha()
            # return (temp_img, temp_rect)

    def __loadAsset(self, name):
        '''The user should not be calling this function directly. Use getAsset(name)'''

        #image, rect = load_image(name)

        MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
        '''Accepts a filename and colorkey, throws an exception if the file does not exist. Returns the pygame.image object
        as well as it's rectangle for manipulation.'''
        fullname = os.path.join(MAIN_DIR, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            raise RuntimeError('Cannot load image:' + fullname)

        # buffer = pygame.surfarray.array3d(image)
        # self.assets[name] = buffer
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
            image = image.convert_alpha()
        return image, image.get_rect()

        #image_buffer = pygame.image.tostring(image, 'RGBA')
        #self.assets[name] = (image_buffer, rect, rect.width, rect.height)
        #return (image, rect)