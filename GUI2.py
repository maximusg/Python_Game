#!/bin/python
import weapon
import player
import enemy
import pygame
from pygame.locals import *
from pygame.compat import geterror
from library import *
import random
import highscore

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.NOFRAME)
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(BLACK)
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)

        #Clock setup
        self.clock = pygame.time.Clock()

        ##load sound bytes
        self.explode = load_sound('explosion.ogg')
        self.fire_spitfire = load_sound('spitfire.ogg')
        self.fire_laser = load_sound('laser.ogg')

    def high_scores(self):
        #get the scoreboard out from storage
        high_scores = highscore.Scoreboard()
        high_scores.readFromFile('highscores.asset')
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('starfield.png')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        hs_list = str(high_scores).split(sep='\n')
        print(hs_list)


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
                text, text_surf = draw_text(line, WHITE, None)
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

        scrollText = pygame.font.Font('OpenSans-Bold.ttf',25)
        text = load_text('openingscroll.asset')

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False ## TODO - needs different handling than SPACE 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False ## TODO - needs different handling than SPACE


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
            self.clock.tick(FRAMERATE)

        gui.menu()

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
        fs_toggle = False ##This here is kinda crappy.
        self.clock.tick() ##need to dump this particular return value of tick() to give accurate time.
        time_since_start = 0
        ##Clock time setup
        while going:
            ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key == K_F1 and DEBUG: ##DEBUG CODE. DO NOT FORGET TO REMOVE
                        #for i in range(200):
                        bad_guy = enemy.enemy('spitfire','enemy.png')
                        enemy_sprites.add(bad_guy)
                    elif event.key == K_F12 and DEBUG:
                        fs_toggle = not fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                    elif event.key == K_PAUSE:
                        self.pause_screen()

            ##Keyboard polling
            keys = pygame.key.get_pressed()
            addBullet = playerShip.control(keys, FRAMERATE)
            if addBullet:
                self.fire_spitfire.play() 
                bullet = playerShip.fire()
                player_bullet_sprites.add(bullet)

            ##Helper to call update() on each sprite in the group.    
            player_sprites.update()
            player_bullet_sprites.update()
            enemy_sprites.update()
            enemy_bullet_sprites.update()
        
            ##Collision/Out of Bounds detection.
            for sprite in player_sprites:
                collision = pygame.sprite.spritecollideany(sprite, enemy_bullet_sprites)
                if collision == None:
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
            
            bg_y1 += .2
            bg_y += .2
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

            for sprite_list in (player_sprites, player_bullet_sprites, enemy_sprites, enemy_bullet_sprites):
                temp_rects = sprite_list.draw(self.screen)

            pygame.display.flip()

            time_since_start += self.clock.tick(FRAMERATE)

 

    def pause_screen(self):
        paused = True
        while paused:
            paused_text, paused_surf = draw_text('***PAUSED***', WHITE, BLACK)
            paused_rect = paused_text.get_rect()
            paused_rect.center = SCREEN_CENTER 
            self.screen.blit(paused_text, paused_rect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_PAUSE or event.key == K_ESCAPE:
                        paused = False
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update(paused_rect)
            self.clock.tick(10)

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
                        
            y1 += 1
            y += 1
            self.screen.blit(bg,(x,y))
            self.screen.blit(bg,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h

            text1, text1_surf = draw_text('PRESS SPACE TO START!', WHITE, BLACK)
            text_rect1 = text1.get_rect()
            text_rect1.center = SCREEN_CENTER
            
            text2, text2_surf = draw_text('PRESS ESC TO EXIT!', WHITE, BLACK)
            text_rect2 = text2.get_rect()
            text_rect2.centerx, text_rect2.top = text_rect1.centerx, text_rect1.bottom 

            text3, text3_surf = draw_text('PRESS S TO SEE THE HALL OF FAME!', WHITE, BLACK)
            text_rect3 = text3.get_rect()
            text_rect3.centerx, text_rect3.top = text_rect2.centerx, text_rect2.bottom

            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(text3, text_rect3)
            
            pygame.display.update()

            self.clock.tick(FRAMERATE//6)
        
        pygame.quit()
            

if __name__=='__main__':

    gui = GUI()
    gui.game_intro()
    


