#IMPORT SECTION
import os
from pathlib import Path
import random
import pygame
from pygame.locals import *
from pygame.compat import geterror
import pickle
import AssetLoader

#CONSTANTS
FRAMERATE = 60

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1920

WINDOW_OPTIONS_FULLSCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE
WINDOW_OPTIONS_WINDOWED = (SCREEN_WIDTH, SCREEN_HEIGHT), 0

COLUMN_WIDTH = SCREEN_WIDTH//5

CWD = Path.cwd()
SAVES_PATH = CWD.joinpath('levels','game_state')
RESOURCES_PATH = CWD.joinpath('resources')
BACKGROUND_PATH = RESOURCES_PATH.joinpath('backgrounds')
EVENT_SCROLL_PATH = RESOURCES_PATH.joinpath('event_scrolls')
FONT_PATH = RESOURCES_PATH.joinpath('fonts')
MUSIC_PATH = RESOURCES_PATH.joinpath('music')
MISC_SPRITES_PATH = RESOURCES_PATH.joinpath('misc_sprites')
SOUND_EFFECT_PATH = RESOURCES_PATH.joinpath('sound_effects')
WEAPON_IMAGES_PATH = RESOURCES_PATH.joinpath('weapon_images')
ITEM_IMAGES_PATH = RESOURCES_PATH.joinpath('item_images')
BOMB_SOUND_PATH = SOUND_EFFECT_PATH.joinpath('bomb_sounds')
BOMB_EXPLOSION_PATH = WEAPON_IMAGES_PATH.joinpath('bomb_explosion')
CHARGE_SHOT_PATH = WEAPON_IMAGES_PATH.joinpath('chargeShot')
UNIT_TESTS_PATH = RESOURCES_PATH.joinpath('unit_test')

DEBUG = False ##DO NOT MESS WITH THIS UNLESS YOU KNOW WHAT YOU'RE DOING.

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (25,25,25)
YELLOW = (255,255,0)

ORIGIN = (0,0)
PLAYER_START = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
SCREEN_CENTER = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

ENEMY_VALUE = 500
BOSS_VALUE = 50000
ITEM_VALUE = 50

ASSET_MANAGER = AssetLoader.AssetLoader()

ENEMY_SPRITE = {
        "diver":1,
        "camper":2, 
        "sleeper":3,
        "crazy":8,
        "crazyReverse": 4,
        "mrVectors": 5,
        "diveBomb": 6,
        "diveStrafe": 7
        }

BULLET_VECTORS = {
    'DEFAULT':['x','x','x'],
    'UP':['x','x',180],
    'DOWN':['x','x',0],
    'LEFT':['x','x',270],
    'RIGHT':['x','x',90]
    }

MASTER_ITEMS = {
    'powerup':('powerup.gif', None),
    'coin':('coin.png', None),
    'spitfire_powerup':('spitfire_powerup.png', 'spitfire'),
    'wavebeam_powerup':('wavebeam_powerup.png', 'waveBeam'),
    'chargeShot_powerup':('chargeShot_powerup.png', 'chargeShot'),
    'healthpack':('healthpack.png', None),
    'bomb_item':('bomb_item.png', None)

    }

#FUNC DEFS
def saveGame(array, stateName="game.sav"):
    '''Pickles array and saves it to filename given in stateName.'''

    with open (SAVES_PATH.joinpath(stateName), "w+b") as write_file:
        pickle.dump(array,write_file)


def loadGame(stateName="game.sav"):
    '''Loads file pointed at by stateName and proceeds to unpickle it. Returns that list to calling function.'''

    location = SAVES_PATH.joinpath(stateName)
    levelState=None
    try:
        with open (location,"r+b") as read_file:
            levelState= pickle.load(read_file)
    except FileNotFoundError as Error:
        raise ("ERROR: LoadGame failed " + Error)
    
    return levelState

def load_text(filename):
    '''Accepts a path to a filename. Returns the text contents of the file as a line-by-line list.'''
    with open(filename) as f:
        return f.readlines()

def load_sound(name):
    '''Accepts a file name and attempts to load it. If pygame.mixer has not been initialized yet, 
    raises an exception. Will throw an exception if the file is not found.
    Returns a pygame.Sound object that can be used.'''
    if not pygame.mixer or not pygame.mixer.get_init():
        raise RuntimeError('Pygame sound mixer not initialized!')
    try:
        sound = pygame.mixer.Sound(str(name))
    except pygame.error:
        raise RuntimeError('Cannot load sound:' + name)
    
    return sound

def load_background_music(filename):
    '''Accepts a filename and will attempt to load that file as background music, repeated infinitely.'''
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=-1)

def draw_text(to_print, text_color, bg_color=None, text_size = 25, bold=False):
    '''Draws the string to_print in the color defined by text_color (can be a defined constant, or an RGB value triple)
       with background color defined by bg_color. If bg_color=None, then no background fill is used. Returns a surface with text
       rendered to it.'''
    if bold:
        text_size -= 1 ##makes things fit better.
        font = pygame.font.Font(str(FONT_PATH.joinpath('OpenSans-Bold.ttf')), text_size)
    else:
        font = pygame.font.Font(str(FONT_PATH.joinpath('OpenSans-Regular.ttf')), text_size)
    text = font.render(str(to_print), True, text_color, bg_color)
    return text

def draw_vertical_bar(color, width, height, bar_percentage = 1, topleft_corner = (0,0)):
    '''Draws a vertical rectangle with (width,height) dimensions and the topleft corner at topleft_corner.
       bar_percentage will accept a float between 0 and 1 for the amount of the bar to fill it (0.6 will still
       draw a border around the entire bar, but only fill 60% with solid color). Returns the surface and its rect to blit.'''
    if not (0 <= bar_percentage <= 1):
        raise RuntimeError('Invalid percentage for vertical bar.')
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
    if not(isinstance(health_percent, float) or isinstance(health_percent, int)) or not(isinstance(shield_percent, float) or isinstance(shield_percent, int)):
        raise RuntimeError('Illegal values for boss bar percentages.')
    if not ((0 <= health_percent <= 1) and (0 <= shield_percent <= 1)):
        raise RuntimeError('Invalid percentage for boss bars.')
    surface = pygame.surface.Surface((width, height))
    surface.fill(GRAY)
    surface.fill(RED, pygame.rect.Rect(1,1,(health_percent) * width-2, height-2))
    surface.fill(BLUE, pygame.rect.Rect(1,1,(shield_percent) * width-2, height-2))
    rect = surface.get_rect()
    rect.topleft = topleft_corner
    return surface, rect

def draw_player_lives(player_lives, topleft_corner = (0,0)):
    '''Draws a graphical representation of the number of player lives remaining. Takes in an integer for the player_lives, and a topleft_corner (x,y) tuple
       if you want to move the location in place (instead of after getting the surface and rect back).'''

    ship = ASSET_MANAGER.getAsset(MISC_SPRITES_PATH.joinpath('SweetShip.png'))
    ship_sprite, ship_rect = ship[0], ship[1]
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
    '''Draws a graphical representation of the number of player bombs remaining. Takes in an integer for the bombs_remaining, and a topleft_corner (x,y) tuple
       if you want to move the location in place (instead of after getting the surface and rect back).'''
    bomb = ASSET_MANAGER.getAsset(WEAPON_IMAGES_PATH.joinpath('bomb.png'))
    bomb_sprite, bomb_rect = bomb[0], bomb[1]
    surface = pygame.surface.Surface((bomb_rect.right * 6, bomb_rect.bottom))
    surface.fill(BLACK)
    surface.blit(bomb_sprite, (0,0))
    text = draw_text('x {}'.format(bombs_remaining), WHITE)
    text_rect = text.get_rect()
    text_rect.left, text_rect.centery = bomb_rect.right+30, bomb_rect.centery
    surface_rect = surface.blit(text, text_rect)
    surface_rect.topleft = topleft_corner
    return surface, surface_rect

def draw_button(text, text_color=BLACK, bg_color=None, topleft_corner = (0,0), bold=False):
    '''Draws a button utilizing draw_text(), then sets its rect's location via topleft_corner. Pass bold=True if you wish to have the text in bold.'''

    button = draw_text(text, text_color, bg_color, bold=bold)
    button_rect = button.get_rect()
    button_rect.topleft = topleft_corner

    return button, button_rect

def draw_instructions():
    '''Draws helper instructions and returns the surface with all of the text pre-blitted.'''

    inst1 = draw_text('Arrow keys to move', WHITE)
    inst2 = draw_text('SPACE key to shoot', WHITE)
    inst3 = draw_text('B key to launch bombs', WHITE)
    inst4 = draw_text('PAUSE to pause', WHITE)
    inst5 = draw_text('ESC to save/quit', WHITE)

    text_block = pygame.surface.Surface((COLUMN_WIDTH, inst1.get_rect().height*5))
    text_block.blit(inst1, ORIGIN)
    text_block.blit(inst2, (0, inst1.get_rect().height))
    text_block.blit(inst3, (0, inst1.get_rect().height*2))
    text_block.blit(inst4, (0, inst1.get_rect().height*3))
    text_block.blit(inst5, (0, inst1.get_rect().height*4))

    return text_block
