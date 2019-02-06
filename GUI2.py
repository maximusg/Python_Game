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
from library import *

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)

        #Clock setup
        self.clock = pygame.time.Clock()

        ##load sound bytes
        self.explode = load_sound('explosn.wav')
        self.fire_shot = load_sound('pewpew.wav')

    def game_intro(self):
        background = pygame.image.load('starfield.png')
        self.screen.blit(background, (0,0))

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False ## TODO - needs different handling than SPACE 
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False ## TODO - needs different handling than SPACE
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    going = False ## TODO - needs different handling than ESCAPE or QUIT

            #BECAUSE BACKGROUND SOUNDS ARE FUN
            if do_sound(0.05):
                self.fire_shot.play()
            if do_sound(0.01):
                self.explode.play()

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            self.screen.blit(background, (0,0))
            scrollText = pygame.font.Font('OpenSans-Bold.ttf',25)
            text = load_text('openingscroll.asset')
            for line in text:
                line = line.strip('\n')
                text_surf, text_rect = text_objects(line, scrollText)
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text_surf, text_rect)
            count += 1
            pygame.display.update()

            if text_rect.bottom < 0:
                going = False
            self.clock.tick(60)

    def main(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg = pygame.image.load('starfield.png').convert()
        background.fill(BLACK)
        background.blit(bg, (0,0))

        #Background sound setup
        pygame.mixer.music.load('roboCop3NES.mp3')
        pygame.mixer.music.play(loops=-1)
        
        ##Initialize ships
        playerShip = player.player('spitfire','SweetShip.png',"arrows")
        bad_guy = enemy.enemy('spitfire','enemy.png')
        
        #Initialize sprite groups
        player_sprites = pygame.sprite.LayeredDirty((playerShip))
        player_bullet_sprites = pygame.sprite.LayeredDirty()
        enemy_sprites = pygame.sprite.LayeredDirty((bad_guy))
        enemy_bullet_sprites = pygame.sprite.LayeredDirty()

        player_sprites.clear(self.screen, background)
        enemy_sprites.clear(self.screen, background)
        player_bullet_sprites.clear(self.screen, background)
        enemy_bullet_sprites.clear(self.screen, background)

        going=True
        while going:
            ##Keyboard polling this way (as opposed to the pygame.event queue) allows multiple (as in up+left) input
            keys = pygame.key.get_pressed()
            addBullet = playerShip.control(keys, FRAMERATE)
            if addBullet:
                self.fire_shot.play() 
                bullet = playerShip.fire()
                player_bullet_sprites.add(bullet)

            ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
            ##Added debug code to spawn enemy sprites at will. -TODO- remove when finished
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
                #elif event.type == KEYDOWN and event.key == K_F1: ##DEBUG CODE. DO NOT FORGET TO REMOVE
                #    bad_guy = enemy()
                #    if len(enemy_sprites) == 0:
                #        enemy_sprites.add(bad_guy)

            text, score_surf = refresh_score(playerShip.point_total)
            self.screen.blit(score_surf, (0,0))
            self.screen.blit(text,(0,0)) 

            ##Helper to call update() on each sprite in the group.    
            player_sprites.update()
            player_bullet_sprites.update()
            enemy_sprites.update()
            enemy_bullet_sprites.update()
        
            ##Collision/Out of Bounds detection.
            for sprite in player_sprites:
                collision = pygame.sprite.spritecollideany(sprite, enemy_sprites)
                if collision:
                    self.explode.play()
                    sprite.visible = 0
                    if sprite.visible == 0:
                        player_sprites.remove(sprite)    
            for sprite in enemy_sprites:
                collision = pygame.sprite.spritecollideany(sprite, player_bullet_sprites)
                if collision:
                    self.explode.play()
                    collision.visible = 0
                    playerShip.point_total += sprite.point_value                    
                    player_bullet_sprites.remove(collision)
                    sprite.visible = 0
                if sprite.visible == 0:
                    enemy_sprites.remove(sprite)         

            player_rects = player_sprites.draw(self.screen)
            player_bullet_rects = player_bullet_sprites.draw(self.screen)
            enemy_rects = enemy_sprites.draw(self.screen)
            enemy_bullet_rects = enemy_bullet_sprites.draw(self.screen)

            pygame.display.update()
            
            ##if pygame.time.get_ticks() % 10 == 0:
            ##    print(self.clock.get_fps())
            
            self.clock.tick(FRAMERATE)
        
        pygame.quit()

    def menu(self):
        background = pygame.image.load('starfield.png')

        background_size = background.get_size()
        screen.convert()
        screen.fill((255,255,255))
        w, h = background_size
        x = 0
        y = 0

        x1 = 0
        y1 = -h

        going = True

        while going:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
            
            y1 += 5
            y += 5
            screen.blit(background,(x,y))
            screen.blit(background,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h
            pygame.display.update()
            self.clock.tick(60)
            
            if pygame.time.get_ticks() % 10 == 0:
                print(self.clock.get_fps())


if __name__=='__main__':
    gui = GUI()
    #gui.game_intro()
    #gui.menu()
    gui.main()

