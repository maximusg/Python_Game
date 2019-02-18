#IMPORT SECTION
import os
import random
import pygame
from pygame.locals import *
from pygame.compat import geterror

#CONSTANTS
FRAMERATE = 60

#SCREEN_HEIGHT = 900
#SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920

WINDOW_OPTIONS_FULLSCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE
WINDOW_OPTIONS_WINDOWED = (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME 

COLUMN_WIDTH = SCREEN_WIDTH//5

BG = 0
GROUND = 1
ITEM = 2
AIR = 3
OVERHEAD = 4

DEBUG = True ##DO NOT MESS WITH THIS UNLESS YOU KNOW WHAT YOU'RE DOING.

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORIGIN = (0,0)
SCREEN_CENTER = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

#MATH for sectors
# DEFAULT_ENEMY_WIDTH = 80 #pixels
# DEFAULT_ENEMY_HEIGHT = 100
# SCREEN_SPACE_WIDTH = COLUMN_WIDTH*3
# ENEMY_SECTORS_AVAIL = SCREEN_SPACE_WIDTH//DEFAULT_ENEMY_HEIGHT
# ENEMY_BUFFER = (SCREEN_SPACE_WIDTH%DEFAULT_ENEMY_HEIGHT)//2
# ENEMY_SECTORS={}
# for i in range(1,ENEMY_SECTORS_AVAIL+1):
#     print("SECTOR ",i,":",ENEMY_BUFFER + DEFAULT_ENEMY_WIDTH*i)

#enemy top screen sectors
ENEMY_SECTORS={ "s1": [106,0], 
                "s2": [186,0],
                "s3": [266,0],
                "s4": [346,0],
                "s5": [426,0],
                "s6": [506,0],
                "s7": [586,0],
                "s8": [666,0],
                "s9": [746,0],
                "s10": [826,0],
                "s11": [906,0],
            }

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

#FUNC DEFS
def load_text(filename):
    '''Accepts a path to a filename. Returns the text contents of the file as a line-by-line list.'''
    with open(filename) as f:
        return f.readlines()

def load_sound(name):
    '''Accepts a file name and attempts to load it. If pygame.mixer has not been initialized yet, 
    returns a dummy class with no sound. Will throw an exception if the file is not found.
    Returns a pygame.Sound object that can be used.'''
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
    '''Accepts a filename and will attempt to load that file as background music, repeated infinitely.'''
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=-1)

def load_image(name, colorkey=None):
    '''Accepts a filename and colorkey, throws an exception if the file does not exist. Returns the pygame.image object
       as well as it's rectangle for manipulation.'''
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

def draw_text(to_print, text_color, bg_color=None):
    '''Draws the string to_print in the color defined by text_color (can be a defined constant, or an RGB value triple)
       with background color defined by bg_color. If bg_color=None, then no background fill is used.'''
    font = pygame.font.Font('OpenSans-Regular.ttf', 25)
    text = font.render(str(to_print), True, text_color)
    text_surf = pygame.Surface(text.get_size())
    if bg_color != None:
        text_surf.fill(bg_color)
    return text, text_surf

def draw_boss_health(sprite):
    bar = pygame.Surface((SCREEN_WIDTH//2-2*COLUMN_WIDTH, 50))
    bar_rect = bar.fill(BLACK)
    ###-TODO- FINISH THIS
