#!/bin/python
import weapon
import player
import enemy
# import launcher
#import control_scheme
import pygame
from pygame.locals import *
from pygame.compat import geterror
#from pathlib import *
#import os
from library import *
import random

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(BLACK)
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)

        #Clock setup
        self.clock = pygame.time.Clock()

        ##load sound bytes
        self.explode = load_sound('explosn.wav')
        self.fire_shot = load_sound('pewpew.wav')

    def game_intro(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('starfield.png')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        scrollText = pygame.font.Font('OpenSans-Bold.ttf',25)
        text = load_text('openingscroll.asset')

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
            if random.random() < 0.05:
                self.fire_shot.play()
            if random.random() < 0.01:
                self.explode.play()

            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

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
        bg, bg_rect = load_image('starfield.png')
        bg_size = bg.get_size()
        bg_w, bg_h = bg_size
        bg_x = 0
        bg_y = 0
        bg_x1 = 0
        bg_y1 = -bg_h
        background.fill(BLACK)
        background.blit(bg, ORIGIN)
        
        column = pygame.Surface((COLUMN_WIDTH, SCREEN_HEIGHT))
        column.fill(BLACK)

        #Background sound setup
        #load_background_music('roboCop3NES.ogg')
        
        ##Initialize ships
        playerShip = player.player('spitfire','SweetShip.png',"arrows")
        bad_guy = enemy.enemy('spitfire','enemy.png')
        #bad_guy.health = 5 ##Verify boss mechanics
        
        #Initialize sprite groups
        player_sprites = pygame.sprite.LayeredDirty((playerShip))
        player_bullet_sprites = pygame.sprite.LayeredDirty()
        enemy_sprites = pygame.sprite.LayeredDirty((bad_guy))
        enemy_bullet_sprites = pygame.sprite.LayeredDirty()

        going=True
        fs_toggle = False
        self.clock.tick() ##need to dump this particular value of tick() to give me accurate time.
        time_since_start = 0
        ##Clock time setup
        while going:
            ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False
                elif event.type == KEYDOWN and event.key == K_F1 and DEBUG: ##DEBUG CODE. DO NOT FORGET TO REMOVE
                    #for i in range(200):
                    bad_guy = enemy.enemy('spitfire','enemy.png')
                    enemy_sprites.add(bad_guy)
                elif event.type == KEYDOWN and event.key == K_F12 and DEBUG:
                    fs_toggle = not fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                    if fs_toggle:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif event.type == KEYDOWN and event.key == K_PAUSE and DEBUG:
                    paused = True
                    while paused:
                        paused_text, paused_surf = draw_text('***PAUSED***', BLACK, WHITE)
                        paused_rect = self.screen.blit(paused_text, (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) ##THIS IS NOT ACTUALLY CENTERED. TODO FIX ME
                        for event in pygame.event.get():
                            if event.type == KEYDOWN and event.key == K_PAUSE:
                                paused = False
                        pygame.display.update(paused_rect)
                        self.clock.tick(10)

            ##Keyboard polling
            keys = pygame.key.get_pressed()
            addBullet = playerShip.control(keys, FRAMERATE)
            if addBullet:
                self.fire_shot.play() 
                bullet = playerShip.fire()
                player_bullet_sprites.add(bullet)

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
                    sprite.health -= 1
                    collision.visible = 0
                    player_bullet_sprites.remove(collision)
                    if sprite.health == 0:
                        self.explode.play()                        
                        playerShip.point_total += sprite.point_value                    
                        sprite.visible = 0
                if sprite.visible == 0:
                    enemy_sprites.remove(sprite)         
            
            ##Start drawing every to the screen
            rect_list = []

            bg_y1 += 5
            bg_y += 5
            self.screen.blit(bg,(bg_x,bg_y))
            self.screen.blit(bg,(bg_x1,bg_y1))
            if bg_y > bg_h:
                bg_y = -bg_h
            if bg_y1 > bg_h:
                bg_y1 = -bg_h

            #self.screen.blit(bg, bg_rect)
            c1 = self.screen.blit(column, ORIGIN)
            c2 = self.screen.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

            text, score_surf = draw_text("Score: "+ str(playerShip.point_total), WHITE, BLACK)
            score_rect = self.screen.blit(score_surf, ORIGIN)
            self.screen.blit(text,ORIGIN)

            if DEBUG:
                debug_text, debug_surf = draw_text('FPS: '+str(round(self.clock.get_fps(), 2)), WHITE, BLACK)
                debug_rect = self.screen.blit(debug_surf, (0, score_rect.bottom))
                self.screen.blit(debug_text, debug_rect)
                rect_list.append(debug_rect)

            for sprite_list in (player_sprites, player_bullet_sprites, enemy_sprites, enemy_bullet_sprites):
                temp_rects = sprite_list.draw(self.screen)
                rect_list.extend(temp_rects)
            rect_list.extend((c1, c2, score_rect, bg_rect))
            
            #pygame.display.update(rect_list)
            pygame.display.flip()

            time_since_start += self.clock.tick_busy_loop(FRAMERATE)

        pygame.quit()

    def menu(self):
        bg, bg_rect = load_image('starfield.png')
        bg_size = bg.get_size()
        w, h = bg_size
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
            
            y1 += 1
            y += 1
            self.screen.blit(bg,(x,y))
            self.screen.blit(bg,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h
            pygame.display.update(bg_rect)

            self.clock.tick(FRAMERATE)
            
            

if __name__=='__main__':
    gui = GUI()
    #gui.game_intro()
    #gui.menu()
    gui.main()

