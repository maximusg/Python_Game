#IMPORT SECTION
import os
import random
import pygame
from pygame.locals import *
from pygame.compat import geterror

#CONSTANTS
FRAMERATE = 60
FS_TOGGLE = False
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1440
COLUMN_WIDTH = SCREEN_WIDTH//10

DEBUG = True ##DO NOT MESS WITH THIS UNLESS YOU KNOW WHAT YOU'RE DOING.

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORIGIN = (0,0)

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

#FUNC DEFS
def load_text(filename):
    with open(filename) as f:
        return f.readlines()

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(MAIN_DIR, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def load_background_music(filename):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=-1)

def random_sound(percentage):
    if random.random() < percentage:
        return True
    return False

def load_image(name, colorkey=None):
    fullname = os.path.join(MAIN_DIR, name)
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

def draw_text(to_print, text_color, bg_color):
    font = pygame.font.Font('OpenSans-Regular.ttf', 25)
    text = font.render(str(to_print), True, WHITE)
    text_surf = pygame.Surface(text.get_size())
    text_surf.fill(BLACK)
    return text, text_surf