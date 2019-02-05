#IMPORT SECTION
import os
import random
import pygame

#CONSTANTS
FRAMERATE = 60
SCREEN_HEIGHT = 786
SCREEN_WIDTH = 1024

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#FUNC DEFS
def load_text(filename):
    with open(filename) as f:
        return f.readlines()

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect().convert()

def load_sound(name):
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(main_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def do_sound(percentage):
    if random.random() < percentage:
        return True
    return False

