#!/bin/python
import weapon
import player
import enemy
import levelLoader
import pygame
from pygame.locals import *
from pygame.compat import geterror
from library import *
import random
import highscore
import item_pickup
# import pyganim

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0],WINDOW_OPTIONS_WINDOWED[1])
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(BLACK)
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)
        self.fs_toggle = True
        self.hs_list = highscore.Scoreboard()
        self.loader = levelLoader.LevelLoader()

        #Clock setup
        self.clock = pygame.time.Clock()

        ##load sound bytes
        self.explode = load_sound('explosion.ogg')
        self.fire_spitfire = load_sound('spitfire.ogg')
        self.fire_laser = load_sound('laser.ogg')

    def game_intro(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('starfield.png')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        story_scroll = load_text('resources/event_scrolls/openingscroll.asset')

        going = True
        count = 0
        pygame.time.wait(1500)

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
            self.clock.tick_busy_loop(FRAMERATE)

        gui.menu()

    def main(self, lives_remaining, curr_score):
        ##Level Loader setup
        starting_events = self.loader.getEvents(0)
        ending_events = self.loader.getEndBehavior()
        player_score = curr_score
        player_lives = lives_remaining    
        bg_filename = starting_events.get('background')
        playerShip = starting_events.get('player')
        if playerShip:
            playerShip = playerShip[0]
        bad_guys = starting_events.get('enemy',[])
        bad_guy_bullets = starting_events.get('bullets',[])

        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image(bg_filename)
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
        # playerShip = player.player('spitfire','SweetShip.png',"arrows")
        # bad_guy = enemy.enemy('spitfire','enemy.png')
        # #bad_guy.health = 5 ##Verify boss mechanics




        #Initialize sprite groups
        player_sprites_invul = pygame.sprite.LayeredDirty(_default_layer = 4)
        player_sprites = pygame.sprite.LayeredDirty(playerShip, _default_layer = 4)
        player_bullet_sprites = pygame.sprite.LayeredDirty(_default_layer = 3)
        enemy_sprites = pygame.sprite.LayeredDirty(bad_guys, _default_layer = 4)
        enemy_bullet_sprites = pygame.sprite.LayeredDirty(bad_guy_bullets, _default_layer = 3)
        items=pygame.sprite.LayeredDirty(_default_layer = 2)


        #spawn a test item
        #collectible = item_pickup.item(500, 500, 1, 'powerup.gif', name='blue_lazer')
        #collectible = item_pickup.item(500, 500, 1)
        #items.add(collectible)


        going=True
        #fs_toggle = False ##This here is kinda crappy.
        self.clock.tick() ##need to dump this particular return value of tick() to give accurate time.
        time_since_start = 0
        next_level = True
        invul_timer = 120 ##frames of invulnerability post-death
        ##Clock time setup
        while going:
            ##Check for end of level conditions
            if ending_events:
                endtime = ending_events.get('time')
                spawn_boss = ending_events.get('boss')
                boss_spawned = False
            else:
                endtime = -1
                spawn_boss = False

            ##check if there is a boss spawned (to figure out when to end the level post boss death)
            if boss_spawned:
                if len(enemy_sprites) == 0:
                    going = False

            ##Beginning of the loop checking for death and lives remaining.
            if len(player_sprites) == 0 and not playerShip.invul_flag:
                player_lives -= 1
                if player_lives:
                    self.death_loop()
                    playerShip = player.player('spitfire','SweetShip.png',"arrows")
                    playerShip.invul_flag = True
                    player_sprites_invul.add(playerShip)
                else:
                    self.game_over(player_score)
                    if self.hs_list.belongsOnList(player_score):
                        name = self.add_to_hs('You\'ve set a high score! Enter your initials!')
                        self.hs_list.add(name, player_score)
                    #break (potentially cleaner than setting going to False)
                    going = False
                    next_level = False

            ##check if the invuln timer is complete
            if invul_timer == 0 and len(player_sprites_invul) != 0:
                playerShip.invul_flag = False
                player_sprites_invul.remove(playerShip)
                player_sprites.add(playerShip)
                invul_timer = 120

            ##Look out for QUIT events (hitting the x in the corner of the window) or escape to quit.
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                    next_level = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                        next_level = False
                    if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                    if event.key == K_PAUSE:
                        self.pause_screen()
                    if DEBUG:
                        if event.key == K_F1: ##DEBUG CODE. DO NOT FORGET TO REMOVE
                            #for i in range(200):
                            bad_guy = enemy.enemy('spitfire','enemy.png')
                            enemy_sprites.add(bad_guy)
                        if event.key == K_F2 and len(player_sprites) == 0:
                            playerShip = player.player('spitfire','SweetShip.png',"arrows")
                            player_sprites.add(playerShip)
                        if event.key == K_F11:
                            enemy_sprites.empty()
                            enemy_bullet_sprites.empty()

            sec_running = time_since_start // 1000 #need seconds since start
            events = self.loader.getEvents(sec_running)
            enemies_to_add = []
            enemy_bullets_to_add = []
            items_to_add = []
            
            if events:
                enemies_to_add = events.get('enemy', [])
                enemy_bullets_to_add = events.get('bullets', [])
                items_to_add = events.get('items', [])
                
            # if events:
            #     try:
            #         enemies_to_add = events['enemy']
            #     except KeyError:
            #         enemies_to_add = []
            #     finally:
            #         try:
            #             enemy_bullets_to_add = events['bullets']
            #         except KeyError:
            #             enemy_bullets_to_add = []
            #         finally:
            #             try:    
            #                 items_to_add = events['items']
            #             except KeyError:
            #                 items_to_add = []

            if sec_running == endtime and spawn_boss:
                pass
                ##spawn the boss
                boss_spawned = True
            if sec_running >= endtime and not spawn_boss:
                if len(enemy_sprites) == 0:
                    going = False ##How do we add some sort of "end of level" animation?
                    
            if enemies_to_add:
                enemy_sprites.add(enemies_to_add)
            if enemy_bullets_to_add:
                enemy_bullet_sprites.add(enemy_bullets_to_add)
            if items_to_add:
                items.add(items_to_add)

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
            for sprite in enemy_sprites:
                bullet = sprite.update()
                if bullet:
                    enemy_bullet_sprites.add(bullet)
            # enemy_sprites.update()
            enemy_bullet_sprites.update()
            items.update()
        
            ##Collision/Out of Bounds detection.
            for sprite in player_sprites:
                collision = pygame.sprite.spritecollideany(sprite, enemy_bullet_sprites)
                if collision == None:
                    collision = pygame.sprite.spritecollideany(sprite, enemy_sprites)
                    if collision:
                        self.explode.play()
                        sprite.visible = 0
                else:
                    self.explode.play()
                    sprite.visible = 0
                if sprite.visible == 0:
                    player_sprites.remove(sprite)
                    
            for sprite in items:
                collision = pygame.sprite.spritecollideany(sprite, player_sprites)
                if collision:
                    # print('you picked up an item', sprite.name)
                    sprite.visible = 0
                    if sprite.is_weapon:
                        playerShip.weapon = weapon.Weapon(sprite.name)
                    items.remove(sprite)
                else:
                    collision = pygame.sprite.spritecollideany(sprite, player_sprites_invul)
                    if collision:
                        sprite.visible = 0
                        if sprite.is_weapon:
                            playerShip.weapon = weapon.Weapon(sprite.name)
                        items.remove(sprite)

            for sprite in enemy_sprites:
                collision = pygame.sprite.spritecollideany(sprite, player_bullet_sprites)
                if collision:
                    sprite.health -= 1
                    collision.visible = 0
                    player_bullet_sprites.remove(collision)
                    if sprite.health == 0:
                        self.explode.play()                        
                        player_score += sprite.point_value
                        sprite.visible = 0
                        item_drop = sprite.getDrop()
                        if item_drop is not None:
                            items.add(item_drop)
                if sprite.visible == 0:
                    enemy_sprites.remove(sprite)     

            for sprite in player_bullet_sprites:
                if sprite.visible == 0:
                    player_bullet_sprites.remove(sprite)    
            
            for sprite in enemy_bullet_sprites:
                if sprite.visible == 0:
                    enemy_bullet_sprites.remove(sprite)

            bg_y1 += 1
            bg_y += 1
            self.screen.blit(bg,(bg_x,bg_y))
            self.screen.blit(bg,(bg_x1,bg_y1))
            if bg_y > bg_h:
                bg_y = -bg_h
            if bg_y1 > bg_h:
                bg_y1 = -bg_h

            #self.screen.blit(bg, bg_rect)
            c1 = self.screen.blit(column, ORIGIN)
            c2 = self.screen.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

            text, score_surf = draw_text("Score: "+ str(player_score), WHITE)
            score_rect = self.screen.blit(score_surf, ORIGIN)
            self.screen.blit(text,ORIGIN)

            lives_text, lives_surf = draw_text('Lives Remaining: '+str(player_lives), WHITE)
            lives_rect = self.screen.blit(lives_surf, (0, score_rect.bottom))
            self.screen.blit(lives_text, lives_rect)

            if DEBUG:
                debug_text, debug_surf = draw_text('FPS: '+str(round(self.clock.get_fps(), 2)), WHITE)
                debug_rect = self.screen.blit(debug_surf, (0, lives_rect.bottom))
                self.screen.blit(debug_text, debug_rect)
            
            player_bullet_sprites.draw(self.screen)
            enemy_bullet_sprites.draw(self.screen)
            items.draw(self.screen)
            if playerShip.invul_flag and invul_timer//6 % 2 == 0: ##allows visual feedback that the player is invulnerable
                player_sprites_invul.draw(self.screen)
            player_sprites.draw(self.screen)
            enemy_sprites.draw(self.screen)

            pygame.display.flip()

            time_since_start += self.clock.tick_busy_loop(FRAMERATE)
            if playerShip.invul_flag:
                invul_timer -= 1
        if next_level:
            self.level_complete()
        return player_lives, player_score, next_level

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
                        pygame.time.wait(500)
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

    def level_complete(self):
        going = True
        start_time = pygame.time.get_ticks()
        while going:
            victory_text, victory_surf = draw_text('Area cleared! Level Complete!', WHITE)
            victory_rect = victory_text.get_rect()
            victory_rect.center = SCREEN_CENTER 
            self.screen.blit(victory_text, victory_rect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update(victory_rect)
            if pygame.time.get_ticks() > start_time + 5000: ###add 5sec for the victory dance.
                going = False
            self.clock.tick(FRAMERATE)


    def death_loop(self):
        dead = True
        while dead:
            dead_text, dead_surf = draw_text('***YOUR SHIP WAS DESTROYED! Press Space to re-deploy!***', WHITE)
            dead_rect = dead_text.get_rect()
            dead_rect.center = SCREEN_CENTER 
            self.screen.blit(dead_text, dead_rect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        dead = False
                        pygame.time.wait(500)
                    if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update(dead_rect)
            self.clock.tick(FRAMERATE)
    
    def game_over(self, player_score):
        dead = True
        while dead:
            dead_text, dead_surf = draw_text('YOU\'VE BEEN DESTROYED! Country Orange has won!', WHITE)
            dead_rect = dead_text.get_rect()
            dead_rect.center = SCREEN_CENTER 
            dead_text2, dead_surf2 = draw_text('Press Space to return to the main menu.', WHITE)
            dead_rect2 = dead_text2.get_rect()
            dead_rect2.centerx, dead_rect2.top = dead_rect.centerx, dead_rect.bottom  
            self.screen.blit(dead_text, dead_rect)
            self.screen.blit(dead_text2, dead_rect2)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        dead = False
                    if event.key == K_F12:
                        self.fs_toggle = not self.fs_toggle ##NEED TO ADD THIS INTO SOME SORT OF CONFIG MENU
                        if self.fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update([dead_rect, dead_rect2])
            self.clock.tick(FRAMERATE)

    def add_to_hs(self, txt):

        def blink(screen):
            for color in [BLACK, WHITE]:
                pygame.draw.circle(box, color, (bx//2, int(by*0.7)), 7, 0)
                self.screen.blit(box, (0, by//2))
                pygame.display.flip()
                pygame.time.wait(300)
        def show_name(screen, name):
            pygame.draw.rect(box, WHITE, (50, 60, bx-100, 20), 0)
            txt_surf = font.render(name, True, BLACK)
            txt_rect = txt_surf.get_rect(center=(bx//2, int(by*0.7)))
            box.blit(txt_surf, txt_rect)
            self.screen.blit(box, (0, by//2))
            pygame.display.flip()
        font = pygame.font.Font('OpenSans-Regular.ttf', 16)
        bx = 480
        by = 100
        # make box
        box = pygame.surface.Surface((bx, by))
        box.fill(BLACK)
        pygame.draw.rect(box, BLACK, (0, 0, bx, by), 1)
        txt_surf = font.render(txt, True, WHITE)
        txt_rect = txt_surf.get_rect(center=(bx//2, int(by*0.3)))
        box.blit(txt_surf, txt_rect)
        name = ""
        show_name(self.screen, name)
        # the input-loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    inkey = event.key
                    if inkey in [13, 271]:  # enter/return key
                        return name
                    elif inkey == 8:  # backspace key
                        name = name[:-1]
                    elif inkey <= 300:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= inkey >= 97:
                            inkey -= 32  # handles CAPITAL input
                        name += chr(inkey)
            if name == "":
                blink(self.screen)
            show_name(self.screen, name)        

    def menu(self):
        bg, bg_rect = load_image('nebula_red.png')
        bg_size = bg.get_size()
        w, h = bg_size
        x = 0
        y = 0
        x1 = 0
        y1 = -h

        going = True
        konami = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a, K_RETURN]
        in_code  = []
        code_accepted = False

        while going:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key == K_SPACE:
                        if code_accepted:
                            gui.level_loop(cheat=True)
                            in_code = []
                            code_accepted = False
                        else:
                            gui.level_loop()
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
                    elif event.key == K_UP:
                        in_code.append(K_UP)
                    elif event.key == K_DOWN:
                        in_code.append(K_DOWN)
                    elif event.key == K_LEFT:
                        in_code.append(K_LEFT)
                    elif event.key == K_RIGHT:
                        in_code.append(K_RIGHT)
                    elif event.key == K_b:
                        in_code.append(K_b)
                    elif event.key == K_a:
                        in_code.append(K_a)
                    elif event.key == K_RETURN:
                        in_code.append(K_RETURN)
                        if in_code == konami:
                            code_accepted = True
                        else:
                            in_code = []
                        
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

            text5, text5_surf = draw_text('CODE ACCEPTED. ENJOY YOUR GAME!', WHITE)
            text_rect5 = text5.get_rect()
            text_rect5.centerx, text_rect5.bottom = text_rect4.centerx, SCREEN_HEIGHT

            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(text3, text_rect3)
            self.screen.blit(text4, text_rect4)
            if code_accepted:
                self.screen.blit(text5, text_rect5)

            pygame.display.update()

            self.clock.tick(FRAMERATE//6)
        
        pygame.quit()

    def credits(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('nebula.jpg')
        with open('resources/event_scrolls/credits.asset') as infile:
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
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('nebula.jpg')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        hs_list = str(self.hs_list).split(sep='\n')

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

    def level_loop(self, cheat=False):
        still_playing = True
        curr_score = 0
        if cheat:
            curr_lives = 100
        else:
            curr_lives = 3
        #event_queue = self.loader.getEvents()
        while still_playing:
            curr_lives, curr_score, next_level = self.main(curr_lives, curr_score)
            if not next_level or not self.loader.nextLevel():
                still_playing = False
            elif next_level and not self.loader.nextLevel():
                still_playing = False
                self.victory()
                if self.hs_list.belongsOnList(curr_score):
                    name = self.add_to_hs('You set a new high score! Enter your initials!')
                    self.hs_list.add(name, curr_score)
                    self.hs_list.writeToFile('resources/event_scrolls/highscores.asset')
        self.loader = levelLoader.LevelLoader()
                #if game won, do something
            
            # if not next_level: ##game over
            #     still_playing = False
            # elif self.loader.nextLevel():
            #     pass   
            # else:
            #     ##end of game
            #     ##self.victory_screen() -TODO-
            #     still_playing = False    

    def victory(self):
        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = load_image('nebula_blue.png')
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        story_scroll = load_text('resources/event_scrolls/ending.asset')

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
            self.clock.tick_busy_loop(FRAMERATE)



if __name__=='__main__':

    gui = GUI()
    gui.game_intro()
    


