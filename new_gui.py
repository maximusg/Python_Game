#!/bin/python

from entity import *
import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
def load_sound(name):
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024,786))
    pygame.display.set_caption('Raiden Clone - Day 0')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    pygame.mixer.music.load('roboCop3NES.mp3')
    pygame.mixer.music.play(loops=-1)
    #explode = load_sound('explosn.wav')
    #fire_shot = load_sound('pewpew.wav')

    clock = pygame.time.Clock()
    player = player_ship()
    allsprites = pygame.sprite.LayeredDirty((player))

    allsprites.clear(screen, background)

    pygame.key.set_repeat(10,10)

    going=True

    bullet_count = 0

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
        if keys[pygame.K_SPACE]:
            #fire_shot.play() ##how do we slow this down to only fire at our assigned ROF?
            if bullet_count % 15 == 0:
                print(str(bullet_count), 'pew!')
            bullet_count += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYUP and event.key == K_SPACE:
                bullet_count = 0
            
        allsprites.update()

        rects = allsprites.draw(screen)
        pygame.display.update(rects)
    
    pygame.quit()

if __name__=='__main__':
    main()

