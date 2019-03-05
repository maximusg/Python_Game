#IMPORT SECTION
import os
from pathlib import Path
import random
import pygame
from pygame.locals import *
from pygame.compat import geterror
import pickle

#CONSTANTS
FRAMERATE = 60

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1920

WINDOW_OPTIONS_FULLSCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE
WINDOW_OPTIONS_WINDOWED = (SCREEN_WIDTH, SCREEN_HEIGHT), 0

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
GRAY = (25,25,25)
YELLOW = (255,255,0)
ORIGIN = (0,0)
SCREEN_CENTER = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


def saveGame(array, stateName="default"):
    cwd = Path.cwd()
    saveLocation = cwd.joinpath('levels', 'game_state')
    with open (saveLocation.joinpath(stateName),"wb") as write_file:
        pickle.dump(array,write_file,)


def loadGame(stateName="default"):
    cwd = Path.cwd()
    saveLocation = cwd.joinpath('levels', 'game_state')
    location = saveLocation.joinpath(stateName)
    levelState=None
    try:
        with open (location,"rb") as read_file:
            levelState= pickle.load(read_file)
    except FileNotFoundError as Error:
        raise ("ERROR: LoadGame failed " + Error)
    
    return levelState

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

def load_image(name, colorkey=-1):
    '''Accepts a filename and colorkey, throws an exception if the file does not exist. Returns the pygame.image object
       as well as it's rectangle for manipulation.'''
    fullname = os.path.join(MAIN_DIR, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    if image.get_alpha():
        image = image.convert_alpha()
        #print('loading {} alpha'.format(name))
    else:
        image = image.convert()
        #print('loading {} non-alpha'.format(name))
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def draw_text(to_print, text_color, bg_color=None, text_size = 25, bold=False):
    '''Draws the string to_print in the color defined by text_color (can be a defined constant, or an RGB value triple)
       with background color defined by bg_color. If bg_color=None, then no background fill is used. Returns a surface with just
       the text (text) and one with the background color (if set) applied.'''
    if bold:
        font = pygame.font.Font('resources/fonts/OpenSans-Regular.ttf', text_size)
    else:
        font = pygame.font.Font('resources/fonts/OpenSans-Regular.ttf', text_size)
    text = font.render(str(to_print), True, text_color, bg_color)
    return text

def draw_vertical_bar(color, width, height, bar_percentage = 1, topleft_corner = (0,0)):
    '''Draws a vertical rectangle with (width,height) dimensions and the topleft corner at topleft_corner.
       bar_percentage will accept a float between 0 and 1 for the amount of the bar to fill it (0.6 will still
       draw a border around the entire bar, but only fill 60% with solid color). Returns the surface and its rect to blit.'''
    if not (0 <= bar_percentage <= 1):
        bar_percentage = 0
        # raise RuntimeError('Invalid percentage for vertical bars.')
    surface = pygame.surface.Surface((width, height))
    surface.fill(GRAY)
    surface.fill(color, pygame.rect.Rect(1,1,width-2,height-2))
    surface.fill(BLACK, pygame.rect.Rect(1,1,width-2,(1-bar_percentage) * height-2))
    rect = surface.get_rect()
    rect.topleft = topleft_corner
    return surface, rect

def draw_boss_bar(width, height, health_percent, shield_percent, topleft_corner = (0,0)):
    '''Draws a vertical rectangle with (width,height) dimensions and the topleft corner at topleft_corner.
       bar_percentage will accept a float between 0 and 1 for the amount of the bar to fill it (0.6 will still
       draw a border around the entire bar, but only fill 60% with solid color). Returns the surface and its rect to blit.'''
    if not ((0 <= health_percent <= 1) or (0 <= shield_percent <= 1)):
        raise RuntimeError('Invalid percentage for boss bars.')
    surface = pygame.surface.Surface((width, height))
    surface.fill(GRAY)
    surface.fill(RED, pygame.rect.Rect(1,1,(health_percent) * width-2, height-2))
    surface.fill(BLUE, pygame.rect.Rect(1,1,(shield_percent) * width-2, height-2))
    rect = surface.get_rect()
    rect.topleft = topleft_corner
    return surface, rect

def draw_player_lives(player_lives, topleft_corner = (0,0)):
    ship_sprite, ship_rect = load_image('CoolShip.png')
    surface = pygame.surface.Surface((ship_rect.right * 3, ship_rect.bottom))
    surface.fill(BLACK)
    surface.blit(ship_sprite, (0,0))
    text = draw_text('x {}'.format(player_lives), WHITE)
    text_rect = text.get_rect()
    text_rect.left, text_rect.centery = ship_rect.right, ship_rect.centery
    surface_rect = surface.blit(text, text_rect)
    surface_rect.topleft = topleft_corner
    return surface, surface_rect

def draw_bombs_remaining(bombs_remaining, topleft_corner = (0,0)):
    bomb_sprite, bomb_rect = load_image('resources/weapon_images/bomb.png')
    surface = pygame.surface.Surface((bomb_rect.right * 6, bomb_rect.bottom))
    surface.fill(BLACK)
    surface.blit(bomb_sprite, (0,0))
    text = draw_text('x {}'.format(bombs_remaining), WHITE)
    text_rect = text.get_rect()
    text_rect.left, text_rect.centery = bomb_rect.right+30, bomb_rect.centery
    surface_rect = surface.blit(text, text_rect)
    surface_rect.topleft = topleft_corner
    return surface, surface_rect

def draw_button(text, text_color=BLACK, bg_color=None, topleft_corner = (0,0)):
    button = draw_text(text, text_color, bg_color)
    button_rect = button.get_rect()
    button_rect.topleft = topleft_corner

    return button, button_rect