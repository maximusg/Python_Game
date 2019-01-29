#!/bin/python

from entity import *
import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *


def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024,786))
    pygame.display.set_caption('Raiden Clone - Day 0')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    clock = pygame.time.Clock()
    player = player_ship()
    allsprites = pygame.sprite.LayeredDirty((player))

    allsprites.clear(screen, background)

    pygame.key.set_repeat(100,10)

    going=True
    while going:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(0,-player.speed)
        if keys[pygame.K_DOWN]:
            player.move(0,player.speed)
        if keys[pygame.K_LEFT]:
            player.move(-player.speed, 0)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed, 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            
        allsprites.update()

        rects = allsprites.draw(screen)
        pygame.display.update(rects)
    
    pygame.quit()

if __name__=='__main__':
    main()

