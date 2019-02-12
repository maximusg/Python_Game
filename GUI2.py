#!/bin/python
import weapon
import player
import enemy
import bg_object
import pygame
from pygame.locals import *
from pygame.compat import geterror
from library import *
import random
import highscore
import item_pickup
import pyganim

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0],WINDOW_OPTIONS_WINDOWED[1])
        self.screen_rect = self.screen.get_rect()
        #self.screen.fill(BLACK)
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)
        self.fs_toggle = False

        #Clock setup
        self.clock = pygame.time.Clock()

        ##load sound bytes
        self.explode = load_sound('explosion.ogg')
        self.fire_spitfire = load_sound('spitfire.ogg')
        self.fire_laser = load_sound('laser.ogg')

    def credits(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('nebula.jpg')
        with open('credits.asset') as infile:
            credit_list = infile.readlines()

        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False ## TODO - needs different handling than SPACE 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False ## TODO - needs different handling than SPACE

            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in credit_list:
                line = line.strip('\n')
                text, text_surf = draw_text(line, WHITE)
                text_rect = text_surf.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0: ###because of the for loop, this is guaranteed to be the last line of text
                going = False
            self.clock.tick(FRAMERATE)


    def high_scores(self):
        #get the scoreboard out from storage
        high_scores = highscore.Scoreboard()
        high_scores.readFromFile('highscores.asset')
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('nebula.jpg')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        hs_list = str(high_scores).split(sep='\n')

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False ## TODO - needs different handling than SPACE 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False ## TODO - needs different handling than SPACE


            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in hs_list:
                text, text_surf = draw_text(line, WHITE)
                text_rect = text_surf.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0:
                going = False
            self.clock.tick(FRAMERATE)

    def game_intro(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('starfield.png')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        story_scroll = load_text('openingscroll.asset')

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False ## TODO - needs different handling than SPACE 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False ## TODO - needs different handling than SPACE
                    if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])


            #BECAUSE BACKGROUND SOUNDS ARE FUN
            if random.random() < 0.01:
                self.fire_spitfire.play()
            if random.random() < 0.01:
                self.fire_laser.play()
            if random.random() < 0.01:
                self.explode.play()

            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in story_scroll:
                line = line.strip('\n')
                text, text_surf = draw_text(line, WHITE)
                text_rect = text_surf.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0:
                going = False
            self.clock.tick(FRAMERATE)

        gui.menu()

    # def main(self):
    #     ##Background setup
    #     background = pygame.Surface(self.screen.get_size())
    #     background = background.convert()
    #     bg, bg_rect = load_image('starfield.png')
    #     bg_size = bg.get_size()
    #     bg_w, bg_h = bg_size
    #     bg_x = 0
    #     bg_y = 0
    #     bg_x1 = 0
    #     bg_y1 = -bg_h
    #     background.fill(BLACK)
    #     background.blit(bg, ORIGIN)
        
    #     column = pygame.Surface((COLUMN_WIDTH, SCREEN_HEIGHT))
    #     column.fill(BLACK)

    #     #Background sound setup
    #     load_background_music('roboCop3NES.ogg')
        
    #     ##Initialize ships
    #     playerShip = player.player('spitfire','SweetShip.png',"arrows")
    #     bad_guy = enemy.enemy('spitfire','enemy.png')
    #     #bad_guy.health = 5 ##Verify boss mechanics


    #     #spawn a test item
    #     collectible = item_pickup.item(500, 500, 1, 'powerup.gif', name='blue_lazer')

    #     #Initialize sprite groups
    #     player_sprites = pygame.sprite.LayeredDirty(playerShip, _default_layer = 4)
    #     player_bullet_sprites = pygame.sprite.LayeredDirty(_default_layer = 3)
    #     enemy_sprites = pygame.sprite.LayeredDirty(bad_guy, _default_layer = 4)
    #     enemy_bullet_sprites = pygame.sprite.LayeredDirty(_default_layer = 3)
    #     items=pygame.sprite.LayeredDirty(collectible, _default_layer = 2)

    #     going=True
    #     #fs_toggle = False ##This here is kinda crappy.
    #     self.clock.tick() ##need to dump this particular return value of tick() to give accurate time.
    #     time_since_start = 0
    #     player_score = 0
    #     ##Clock time setup
    #     while going:
    #         ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
    #         for event in pygame.event.get():
    #             if event.type == QUIT:
    #                 going = False
    #             elif event.type == KEYDOWN:
    #                 if event.key == K_ESCAPE:
    #                     going = False
    #                 if event.key == K_F12:
    #                     self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
    #                     if self.fs_toggle:
    #                         pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
    #                     else:
    #                         pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
    #                 if event.key == K_PAUSE:
    #                     self.pause_screen()
    #                 if DEBUG:
    #                     if event.key == K_F1: ##DEBUG CODE. DO NOT FORGET TO REMOVE
    #                         #for i in range(200):
    #                         bad_guy = enemy.enemy('spitfire','enemy.png')
    #                         enemy_sprites.add(bad_guy)
    #                     if event.key == K_F2 and len(player_sprites) == 0:
    #                         playerShip = player.player('spitfire','SweetShip.png',"arrows")
    #                         player_sprites.add(playerShip)

    #         ##Keyboard polling
    #         keys = pygame.key.get_pressed()
    #         addBullet = playerShip.control(keys, FRAMERATE)
    #         if addBullet and len(player_sprites) != 0:
    #             self.fire_spitfire.play() 
    #             bullet = playerShip.fire()
    #             player_bullet_sprites.add(bullet)

    #         ##Helper to call update() on each sprite in the group.    
    #         player_sprites.update()
    #         player_bullet_sprites.update()
    #         enemy_sprites.update()
    #         enemy_bullet_sprites.update()
    #         items.update()
        
    #         ##Collision/Out of Bounds detection.
    #         for sprite in player_sprites:
    #             collision = pygame.sprite.spritecollideany(sprite, enemy_bullet_sprites)
    #             if collision == None:
    #                 collision = pygame.sprite.spritecollideany(sprite, enemy_sprites)
    #                 if collision:
    #                     self.explode.play()
    #                     sprite.visible = 0
    #             if sprite.visible == 0:
    #                 player_sprites.remove(sprite)
                    
    #         for sprite in items:
    #             collision = pygame.sprite.spritecollideany(sprite, player_sprites)
    #             if collision:
    #                 print('you picked up an item', sprite.name)
    #                 sprite.visible = 0
    #                 if sprite.is_weapon:
    #                     playerShip.weapon = weapon.Weapon(sprite.name)
    #                 items.remove(sprite)

    #         for sprite in enemy_sprites:
    #             collision = pygame.sprite.spritecollideany(sprite, player_bullet_sprites)
    #             if collision:
    #                 sprite.health -= 1
    #                 collision.visible = 0
    #                 player_bullet_sprites.remove(collision)
    #                 if sprite.health == 0:
    #                     self.explode.play()                        
    #                     player_score += sprite.point_value
    #                     sprite.visible = 0
    #             if sprite.visible == 0:
    #                 enemy_sprites.remove(sprite)     

    #         for sprite in player_bullet_sprites:
    #             if sprite.visible == 0:
    #                 player_bullet_sprites.remove(sprite)    
            
    #         for sprite in enemy_bullet_sprites:
    #             if sprite.visible == 0:
    #                 enemy_bullet_sprites.remove(sprite)

    #         bg_y1 += 1
    #         bg_y += 1
    #         self.screen.blit(bg,(bg_x,bg_y))
    #         self.screen.blit(bg,(bg_x1,bg_y1))
    #         if bg_y > bg_h:
    #             bg_y = -bg_h
    #         if bg_y1 > bg_h:
    #             bg_y1 = -bg_h

    #         #self.screen.blit(bg, bg_rect)
    #         c1 = self.screen.blit(column, ORIGIN)
    #         c2 = self.screen.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

    #         text, score_surf = draw_text("Score: "+ str(player_score), WHITE)
    #         score_rect = self.screen.blit(score_surf, ORIGIN)
    #         self.screen.blit(text,ORIGIN)

    #         if DEBUG:
    #             debug_text, debug_surf = draw_text('FPS: '+str(round(self.clock.get_fps(), 2)), WHITE)
    #             debug_rect = self.screen.blit(debug_surf, (0, score_rect.bottom))
    #             self.screen.blit(debug_text, debug_rect)

    #         for sprite_list in (player_bullet_sprites, enemy_bullet_sprites, items, player_sprites, enemy_sprites):
    #             temp_rects = sprite_list.draw(self.screen)
    #             #pyganim animation here?


    #         pygame.display.flip()

    #         time_since_start += self.clock.tick(FRAMERATE) 

    def main(self):
        ##Background setup
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background = background.convert()
        bg, bg_rect = load_image('starfield.png')

        background.blit(bg, ORIGIN)

        column = pygame.Surface((COLUMN_WIDTH, SCREEN_HEIGHT))
        column.fill(BLACK)

        # background.blit(column, ORIGIN)
        # background.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

        #Ship setup
        playerShip = player.player('spitfire','SweetShip.png',"arrows")

        ##Build our groups
        bg_sprites = pygame.sprite.LayeredDirty()
        player_sprites = pygame.sprite.LayeredDirty()
        player_bullet_sprites = pygame.sprite.LayeredDirty()
        enemy_sprites = pygame.sprite.LayeredDirty()
        enemy_bullet_sprites = pygame.sprite.LayeredDirty()

        player_sprites.add(playerShip)

        #set the background
        bg_sprites.clear(self.screen, background)
        player_sprites.clear(self.screen, background)
        enemy_sprites.clear(self.screen, background)
        player_bullet_sprites.clear(self.screen, background)
        enemy_bullet_sprites.clear(self.screen, background)

        #variables that need to be outside the loop
        fs_toggle = True
        player_score = 0
        
        going = True
        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])

            if random.random() < 0.01:
                new_x = random.randint(COLUMN_WIDTH, SCREEN_WIDTH-COLUMN_WIDTH)
                new_bg_sprite = bg_object.bg_object(new_x, 0, 4, 'asteroid.png')
                bg_sprites.add(new_bg_sprite)
                print('made an asteroid!')

            ##Keyboard polling
            keys = pygame.key.get_pressed()
            addBullet = playerShip.control(keys, FRAMERATE)
            if addBullet and len(player_sprites) != 0:
                self.fire_spitfire.play() 
                bullet = playerShip.fire()
                player_bullet_sprites.add(bullet)

            bg_sprites.update()
            player_sprites.update()
            player_bullet_sprites.update()
            enemy_sprites.update()
            enemy_bullet_sprites.update()

            c1 = self.screen.blit(column, ORIGIN)
            c2 = self.screen.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

            text, score_surf = draw_text("Score: "+ str(player_score), WHITE)
            #text, score_surf = draw_text("Score: ", WHITE)
            score_rect = self.screen.blit(score_surf, ORIGIN)
            self.screen.blit(text,ORIGIN)
            if DEBUG:
                debug_text, debug_surf = draw_text('FPS: '+str(round(self.clock.get_fps(), 2)), WHITE)
                debug_rect = self.screen.blit(debug_surf, (0, score_rect.bottom))
                self.screen.blit(debug_text, debug_rect)

            bg_rects = bg_sprites.draw(self.screen)
            player_rects = player_sprites.draw(self.screen)
            pl_bullet_rects = player_bullet_sprites.draw(self.screen)
            enemy_rects = enemy_sprites.draw(self.screen)
            en_bullet_rects = enemy_bullet_sprites.draw(self.screen)

            allsprites = []
            for sprite_list in (bg_rects, pl_bullet_rects, en_bullet_rects, player_rects, enemy_rects):
                for sprite in sprite_list:
                    allsprites.append(sprite)
            allsprites.append(score_rect)
            if DEBUG:
                allsprites.append(debug_rect)
            allsprites.extend([c1,c2])

            pygame.display.update(allsprites)

            for sprite in bg_sprites:
                if sprite.visible == 0:
                    bg_sprites.remove(sprite)
            for sprite in player_bullet_sprites:
                if sprite.visible == 0:
                    player_bullet_sprites.remove(sprite)
            for sprite in enemy_bullet_sprites:
                if sprite.visible == 0:
                    enemy_bullet_sprites.remove(sprite)

            # pygame.display.update(score_rect)
            # if DEBUG:
            #     pygame.display.update(debug_rect)
            # pygame.display.update(bg_rects)
            # pygame.display.update(player_rects)
            # pygame.display.update(enemy_rects)

            self.clock.tick_busy_loop(FRAMERATE)


        

    def pause_screen(self):
        paused = True
        while paused:
            paused_text, paused_surf = draw_text('***PAUSED***', WHITE)
            paused_rect = paused_text.get_rect()
            paused_rect.center = SCREEN_CENTER 
            self.screen.blit(paused_text, paused_rect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_PAUSE or event.key == K_ESCAPE:
                        paused = False
                if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update(paused_rect)
            self.clock.tick(FRAMERATE)

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
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key == K_SPACE:
                        gui.main()
                    elif event.key == K_s:
                        gui.high_scores()
                    elif event.key == K_c:
                        gui.credits()
                    elif event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                        
            y1 += 1
            y += 1
            self.screen.blit(bg,(x,y))
            self.screen.blit(bg,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h

            text1, text1_surf = draw_text('PRESS SPACE TO START!', WHITE)
            text_rect1 = text1.get_rect()
            text_rect1.center = SCREEN_CENTER
            
            text2, text2_surf = draw_text('PRESS ESC TO EXIT!', WHITE)
            text_rect2 = text2.get_rect()
            text_rect2.centerx, text_rect2.top = text_rect1.centerx, text_rect1.bottom 

            text3, text3_surf = draw_text('PRESS S TO SEE THE HALL OF FAME!', WHITE)
            text_rect3 = text3.get_rect()
            text_rect3.centerx, text_rect3.top = text_rect2.centerx, text_rect2.bottom

            text4, text4_surf = draw_text('PRESS C TO SEE THE CREDITS!', WHITE)
            text_rect4 = text4.get_rect()
            text_rect4.centerx, text_rect4.top = text_rect3.centerx, text_rect3.bottom

            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(text3, text_rect3)
            self.screen.blit(text4, text_rect4)

            pygame.display.update()

            self.clock.tick(FRAMERATE//6)
        
        pygame.quit()
            

if __name__=='__main__':

    gui = GUI()
    #gui.game_intro()
    gui.main()
    pygame.quit()
    


