#!/bin/python
import weapon
import player
import enemy
# import launcher
import control_scheme
import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
#import hud

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
    ##CONSTANTS
    FRAMERATE = 60
    ##Initialize pygame, set up the screen.
    pygame.init()
    screen = pygame.display.set_mode((1024,786))
    pygame.display.set_caption('Raiden Clone - Day 0')
    pygame.mouse.set_visible(False)
    ##Background setup
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    ##Background music setup, load sound bytes
    pygame.mixer.music.load('roboCop3NES.mp3')
    pygame.mixer.music.play(loops=-1)
    explode = load_sound('explosn.wav')
    fire_shot = load_sound('pewpew.wav')
    ##Initialize clock
    clock = pygame.time.Clock()
    ##Initialize ships
    
    playerShip = player.player('spitfire','SweetShip.png',"arrows")
    bad_guy = enemy.enemy('spitfire','enemy.png')
    #Initialize sprite groups
    player_sprites = pygame.sprite.LayeredDirty((playerShip))
    player_bullet_sprites = pygame.sprite.LayeredDirty()
    enemy_sprites = pygame.sprite.LayeredDirty((bad_guy))
    enemy_bullet_sprites = pygame.sprite.LayeredDirty()

    player_sprites.clear(screen, background)
    enemy_sprites.clear(screen, background)
    player_bullet_sprites.clear(screen, background)
    enemy_bullet_sprites.clear(screen, background)


    going=True

    while going:

        #update the hud
        #myHUD.showHUD()

        ##Force FRAMERATE ticks per second
        clock.tick(FRAMERATE)

        ##Keyboard polling this way (as opposed to the pygame.event queue) allows multiple (as in up+left) input
        addBullet = playerShip.control(FRAMERATE)
        if addBullet:
            fire_shot.play() 
            bullet = playerShip.fire()
            player_bullet_sprites.add(bullet)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     playerShip.move(0,-playerShip.speed)
        # if keys[pygame.K_DOWN]:
        #     player.move(0,player.speed)
        # if keys[pygame.K_LEFT]:
        #     player.move(-player.speed, 0)
        # if keys[pygame.K_RIGHT]:
        #     player.move(player.speed, 0)
        # if keys[pygame.K_SPACE]:
        #     if bullet_count % (int(FRAMERATE/player.weapon.rof)) == 0:
        #         fire_shot.play() 
        #         bullet = player.fire()
        #         player_bullet_sprites.add(bullet)
        #     bullet_count += 1

        ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
        ##Added debug code to spawn enemy sprites at will. -TODO- remove when finished
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            # elif event.type == KEYDOWN and event.key == K_F1: ##DEBUG CODE. DO NOT FORGET TO REMOVE
            #     bad_guy = enemy()
            #     if len(enemy_sprites) == 0:
            #         enemy_sprites.add(bad_guy)
            #elif event.type == KEYUP and event.key == K_SPACE:
            #    bullet_count = 0

            
        ##Helper to call update() on each sprite in the group.    
        player_sprites.update()
        player_bullet_sprites.update()
        enemy_sprites.update()
        enemy_bullet_sprites.update()
      
        ##Collision/Out of Bounds detection.
        for sprite in player_bullet_sprites:
            if sprite.visible == 0:
                player_bullet_sprites.remove(sprite)
        for sprite in enemy_bullet_sprites:
            if sprite.visible == 0:
                enemy_bullet_sprites.remove(sprite)
        for sprite in player_sprites:
            collision = pygame.sprite.spritecollideany(sprite, enemy_sprites)
            if collision:
                explode.play()
                sprite.visible = 0
            if sprite.visible == 0:
                player_sprites.remove(sprite)    
        for sprite in enemy_sprites:
            collision = pygame.sprite.spritecollideany(sprite, player_bullet_sprites)
            if collision:
                explode.play()
                collision.visible = 0
                player_bullet_sprites.remove(collision)
                sprite.visible = 0
            if sprite.visible == 0:
                enemy_sprites.remove(sprite)         

        player_rects = player_sprites.draw(screen)
        player_bullet_rects = player_bullet_sprites.draw(screen)
        enemy_rects = enemy_sprites.draw(screen)
        enemy_bullet_rects = enemy_bullet_sprites.draw(screen)

        pygame.display.update(player_rects)
        pygame.display.update(player_bullet_rects)
        pygame.display.update(enemy_rects)
        pygame.display.update(enemy_bullet_rects)
    
        
        if pygame.time.get_ticks() % 60 == 0:
            print(clock.get_fps())

    pygame.quit()

if __name__=='__main__':
    main()

