from pathlib import *
import pygame
from pygame.locals import *
from pygame.compat import geterror

##CONSTANTS
FRAMERATE = 60
main_dir = Path('.')

def load_image(name, colorkey=None):
    fullname = main_dir.joinpath(name)
    try:
        image = pygame.image.load(str(fullname))
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = main_dir.joinpath(name)
    try:
        sound = pygame.mixer.Sound(str(fullname))
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def check_bounds(rect, area):
    return rect.top >= 0 and rect.bottom <= area.bottom and rect.left >= 0 and rect.right <= area.right