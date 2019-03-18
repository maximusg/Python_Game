import pygame
import sys
from pygame.locals import *
from pygame.compat import geterror
from library import *
import Entity
import weapon
import explosion
import bomb_explosion
import levelLoader
import highscore
import random

class GUI(object):
    '''Class controlling the entire window setting and game state setup of the game. '''

    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0],WINDOW_OPTIONS_WINDOWED[1])
        self.screen_rect = self.screen.get_rect()
        self.hs_list = highscore.Scoreboard()
        self.loader = None

        #Clock setup
        self.clock = pygame.time.Clock()

        #private variables
        self.__fs_toggle = False

        self.screen.fill(BLACK)
        pygame.display.set_caption('Raiden Clone - Day 0')
        pygame.mouse.set_visible(False)

        ##load sound bytes
        self.explode = load_sound(SOUND_EFFECT_PATH.joinpath('explosion.ogg'))
        self.fire_spitfire = load_sound(SOUND_EFFECT_PATH.joinpath('spitfire.ogg'))
        self.fire_laser = load_sound(SOUND_EFFECT_PATH.joinpath('laser.ogg'))

    @property
    def screen(self):
        return self.__screen

    @property
    def screen_rect(self):
        return self.__screen_rect

    @property
    def hs_list(self):
        return self.__hs_list

    @property
    def loader(self):
        return self.__loader

    @property
    def clock(self):
        return self.__clock

    @screen.setter
    def screen(self, value):
        if not isinstance(value, pygame.surface.Surface):
            raise RuntimeError('Screen must be a pygame Surface!')
        self.__screen = value
    
    @screen_rect.setter
    def screen_rect(self, value):
        if not isinstance(value, pygame.rect.Rect):
            raise RuntimeError('Screen rect must be a pygame Rect!')
        self.__screen_rect = value

    @hs_list.setter
    def hs_list(self, value):
        if not isinstance(value, highscore.Scoreboard):
            raise RuntimeError('High Score list attemped initialization with something other than a high score list.')
        self.__hs_list = value

    @loader.setter
    def loader(self, value):
        if not isinstance(value, levelLoader.LevelLoader) and value != None:
            raise RuntimeError('Invalid level loader initialization')
        self.__loader = value

    @clock.setter
    def clock(self, value):
        if not isinstance(value, type(pygame.time.Clock())):
            raise RuntimeError('Illegal value for clock. Must be pygame.time.Clock.')
        self.__clock = value    

    def game_intro(self):
        '''Invokes game introduction state.'''

        ##Background setup
        #Background sound setup
        load_background_music(str(MUSIC_PATH.joinpath('roboCop3NES.ogg')))
        pygame.mixer.music.set_volume(0.10)
        
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath('starfield.png'))
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        story_scroll = load_text(EVENT_SCROLL_PATH.joinpath('openingscroll.asset'))

        going = True
        count = 0
        pygame.time.wait(500)

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False 
                        
                    if event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle 
                        if self.__fs_toggle:
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
                text = draw_text(line, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0:
                going = False
            self.clock.tick_busy_loop(FRAMERATE)

        gui.menu()

    def main(self, lives_remaining, curr_score, currPlayerShip, currTime = 0):
        '''Invokes main game state. Takes lives_remaining (lives remaining), curr_score (current score), currPlayerShip (a reference to the current player entity), and currTime (in seconds).'''

        ##Level Loader setup
        starting_events = self.loader.getEvents(0)
        ending_events = self.loader.getEndBehavior()
        player_score = curr_score
        player_lives = lives_remaining    
        bg_filename = starting_events.get('background')
        if currPlayerShip:
            playerShip = currPlayerShip
            playerShip.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
        else:
            playerShip = starting_events.get('player')
            if playerShip:
                playerShip = playerShip[0]

        ##Check for end of level conditions
        if ending_events:
            endtime = ending_events.get('time')
            spawn_boss = ending_events.get('boss')
            boss_spawned = False
        else:
            endtime = -1
            spawn_boss = False

        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath(bg_filename))
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

        inst_block = draw_instructions()

        #Initialize sprite groups
        player_sprites_invul = pygame.sprite.Group()
        player_sprites = pygame.sprite.GroupSingle(playerShip)
        player_bullet_sprites = pygame.sprite.Group()
        player_bomb_sprites = pygame.sprite.Group() #not sure if bombs should be on the lowest layer
        bomb_explosion_sprites = pygame.sprite.Group() # the bomb explosion should damage enemies on collision, so it is on the same layer as enemies
        enemy_sprites = pygame.sprite.Group()
        boss_sprites = pygame.sprite.GroupSingle()
        enemy_bullet_sprites = pygame.sprite.Group()
        items=pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        chargeShot_Anim = pygame.sprite.GroupSingle()

        going=True
        self.clock.tick() ##need to dump this particular return value of tick() to give accurate time.
        time_since_start = currTime * 1000 #convert to milliseconds
        next_level = True
        invul_timer = 120 ##frames of invulnerability post-death
        regen_timer = 6
        bomb_timer = 120
        time_to_end = 9999 ## No levels this long, so effectively infinity.
        ##Clock time setup
        while going:
            
            ##check if there is a boss spawned (to figure out when to end the level post boss death)
            if boss_spawned and time_to_end == 9999:
                if len(boss_sprites) == 0:
                    time_to_end = time_since_start//1000 + 5
            if time_since_start//1000 == time_to_end:
                going = False

            ##Beginning of the loop checking for death and lives remaining.
            if len(player_sprites) == 0 and not playerShip.invul_flag:
                player_lives -= 1
                if player_lives:
                    self.death_loop()
                    playerShip = Entity.Player('spitfire',MISC_SPRITES_PATH.joinpath('SweetShip.png'),"arrows") 
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
                    pygame.mouse.set_visible(True) ##We need the mouse here.
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # going = False
                        # next_level = False
                        pygame.mouse.set_visible(True) ##We need the mouse here.
                        going, next_level = self.ask_to_save(playerShip.health, playerShip.shield, playerShip.weapon.name, playerShip.bombs_remaining, player_score, player_lives, time_since_start//1000)
                    if event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle 
                        if self.__fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                    if event.key == K_PAUSE:
                        self.pause_screen()
                    if DEBUG:
                        if event.key == K_F2 and len(player_sprites) == 0:
                            playerShip = Entity.Player('spitfire',MISC_SPRITES_PATH.joinpath('SweetShip.png'),"arrows")
                            player_sprites.add(playerShip)
                        if event.key == K_F11:
                            enemy_sprites.empty()
                            enemy_bullet_sprites.empty()

            sec_running = time_since_start // 1000 #need seconds since start
            events = self.loader.getEvents(sec_running)
            enemies_to_add = []
            boss_to_add = []
            enemy_bullets_to_add = []
            items_to_add = []
            
            if events:
                enemies_to_add = events.get('enemy', [])
                boss_to_add = events.get('boss_sprite', [])
                enemy_bullets_to_add = events.get('bullets', [])
                items_to_add = events.get('items', [])
                
            if sec_running >= endtime and not spawn_boss:
                if len(enemy_sprites) == 0 and len(enemy_bullet_sprites) == 0:
                    going = False
                    
            if enemies_to_add:
                enemy_sprites.add(enemies_to_add)
            if boss_to_add:
                boss_spawned = True
                boss_sprites.add(boss_to_add)
            if enemy_bullets_to_add:
                enemy_bullet_sprites.add(enemy_bullets_to_add)
            if items_to_add:
                items.add(items_to_add)

            #chargeShot specific weapon firing
            if playerShip.weapon.name in playerShip.weapon.chargeShot_dic:
                if playerShip.weapon.chargeShot_charging_flag == True:
                    keys = pygame.key.get_pressed()
                    if not keys[pygame.K_SPACE]:
                        playerShip.weapon.chargeShot_charging_flag = False
                        playerShip.weapon.chargeShot_firing_flag = True

            if playerShip.weapon.name in playerShip.weapon.chargeShot_dic:
                if playerShip.weapon.chargeShot_firing_flag == True:
                    if playerShip.weapon.chargeShot_counter >= 0:
                        bullet = playerShip.fire()
                        bullet.damage = playerShip.weapon.weapon_damage
                        #print(bullet.damage)
                        player_bullet_sprites.add(bullet)
                        playerShip.weapon.chargeShot_counter -= 1
                    else:
                        playerShip.weapon.chargeShot_firing_flag = False


            keys = pygame.key.get_pressed()
            addBullet = playerShip.control(keys, FRAMERATE)
            if addBullet:
                #special behavior for chargeShot
                if playerShip.weapon.name in playerShip.weapon.chargeShot_dic:
                    #this is the chargeShot "charging" code
                    if playerShip.weapon.chargeShot_firing_flag is False:
                        playerShip.weapon.chargeShot_charging_flag = True
                        if playerShip.weapon.chargeShot_counter <= playerShip.weapon.chargeShot_counter_max:
                            playerShip.weapon.chargeShot_counter += playerShip.weapon.chargeShot_counter_rate
                            #print(playerShip.weapon.name, playerShip.weapon.chargeShot_counter)


                        if playerShip.weapon.chargeShot_anim_visible is False:
                            playerShip.weapon.chargeShot_anim_visible = True
                            new_charging = weapon.ChargingAnim(playerShip.rect.centerx,playerShip.rect.centery, playerShip)
                            chargeShot_Anim.add(new_charging)

                #normal bullet behavior
                else:
                    self.fire_spitfire.play()
                    bullet = playerShip.fire()
                    player_bullet_sprites.add(bullet)

            if playerShip.drop_bomb_flag is True:
                bomb = playerShip.drop_bomb()
                bomb.play_sound()
                playerShip.drop_bomb_flag = False
                player_bomb_sprites.add(bomb)
                playerShip.curr_bomb = bomb

            if playerShip.curr_bomb is not None and playerShip.curr_bomb.bomb_explode is True:
                new_explosion = bomb_explosion.BombExplosion(playerShip.curr_bomb.centerx,playerShip.curr_bomb.centery)
                new_explosion.play_sound()
                bomb_explosion_sprites.add(new_explosion)
                playerShip.curr_bomb.bomb_explode = False

                playerShip.curr_bomb = None


            ##Helper to call update() on each sprite in the group.    
            # player_sprites.update()
            player_damage = playerShip.update()
            if player_damage:
                explosions.add(player_damage)
            player_bullet_sprites.update()
            player_bomb_sprites.update()
            for sprite in enemy_sprites:
                bullet = sprite.update()
                if bullet:
                  enemy_bullet_sprites.add(bullet)
            for sprite in boss_sprites:
                damage, bullets = sprite.update(playerShip.rect.center)
                if damage:
                    explosions.add(damage)
                if bullets:
                    enemy_bullet_sprites.add(bullets)
            enemy_bullet_sprites.update()
            items.update()
            explosions.update()
            bomb_explosion_sprites.update()
            chargeShot_Anim.update()
        
            ##Collision/Out of Bounds detection.
            if player_sprites.sprite != None:
                collision = pygame.sprite.spritecollideany(player_sprites.sprite, enemy_bullet_sprites)
                if collision:
                    self.explode.play()
                    playerShip.take_damage(5)
                    collision.kill()
                else:
                    collision = pygame.sprite.spritecollideany(player_sprites.sprite, enemy_sprites)
                    if collision:
                        self.explode.play()
                        playerShip.take_damage(1)
                    else:
                        collision = pygame.sprite.spritecollideany(player_sprites.sprite, boss_sprites)
                        if collision:
                            self.explode.play()
                            playerShip.take_damage(1)
                if playerShip.health <= 0:
                    chargeShot_Anim.empty()
                    playerShip.kill()
                    
            for sprite in items:
                collision = pygame.sprite.spritecollideany(sprite, player_sprites)
                if collision:
                    sprite.visible = 0
                    player_score += sprite.value
                    if sprite.checkWeapon():
                        upgrade = weapon.upgrade(sprite.weapon_name, playerShip.weapon.name)
                        playerShip.weapon = weapon.Weapon(upgrade)
                    if sprite.checkBomb():
                        playerShip.bombs_remaining += 1
                    if sprite.checkHealthPack():
                        if playerShip.health < playerShip.max_health:
                            new_health = playerShip.health + playerShip.healthpack
                            if new_health >= playerShip.max_health:
                                playerShip.health = playerShip.max_health
                            else:
                                playerShip.health += playerShip.healthpack
                    sprite.kill()

                else:
                    collision = pygame.sprite.spritecollideany(sprite, player_sprites_invul)
                    if collision:
                        sprite.visible = 0
                        if sprite.checkWeapon():
                            upgrade = weapon.upgrade(sprite.weapon_name, playerShip.weapon.name)
                            playerShip.weapon = weapon.Weapon(upgrade)
                        sprite.kill()

            for sprite in enemy_sprites:
                collision = pygame.sprite.spritecollideany(sprite, player_bullet_sprites)
                if collision:
                    sprite.take_damage(playerShip.weapon.getDamage(playerShip.weapon.name))

                    collision.visible = 0
                    collision.kill()
                else:
                    collision = pygame.sprite.spritecollideany(sprite, bomb_explosion_sprites)
                    if collision:
                        sprite.take_damage(playerShip.weapon.getDamage('bomb'))

                if sprite.health <= 0:
                    new_explosion = explosion.ExplosionSprite(sprite.rect.centerx,sprite.rect.centery)
                    new_explosion.play_sound() 
                    explosions.add(new_explosion)                        
                    player_score += sprite.value
                    item_drop = sprite.getDrop()
                    if item_drop is not None:
                        items.add(item_drop)
                if sprite.visible == 0:
                    sprite.kill()
 
            if boss_sprites.sprite != None:
                collision_dict = pygame.sprite.groupcollide(player_bullet_sprites, boss_sprites, True, False)
                for key in collision_dict:
                    boss_sprites.sprite.take_damage(key.damage)
                collision = pygame.sprite.spritecollideany(boss_sprites.sprite, bomb_explosion_sprites)
                if collision:
                    boss_sprites.sprite.take_damage(2)
                if boss_sprites.sprite.health <= 0:
                    new_explosion = explosion.ExplosionSprite(sprite.rect.centerx,sprite.rect.centery)
                    new_explosion.play_sound() 
                    explosions.add(new_explosion)                        
                    player_score += boss_sprites.sprite.point_value
                    boss_sprites.sprite.kill()  

            #sprite cleanup
            for sprite in player_bullet_sprites:
                if sprite.visible == 0:
                    sprite.kill()    
            
            for sprite in enemy_bullet_sprites:
                if sprite.visible == 0:
                    sprite.kill()

            for sprite in explosions:
                if sprite.visible == 0:
                    sprite.kill()

            for sprite in player_bomb_sprites:
                if sprite.visible == 0:
                    sprite.kill()

            for sprite in bomb_explosion_sprites:
                if sprite.visible == 0:
                    sprite.kill()

            for sprite in items:
                if sprite.visible == 0:
                    sprite.kill()

            for sprite in chargeShot_Anim:
                if sprite.visible == 0:
                    sprite.kill()

            bg_y1 += 1
            bg_y += 1
            self.screen.blit(bg,(bg_x,bg_y))
            self.screen.blit(bg,(bg_x1,bg_y1))
            if bg_y > bg_h:
                bg_y = -bg_h
            if bg_y1 > bg_h:
                bg_y1 = -bg_h

            if boss_spawned and boss_sprites.sprite != None:
                boss_bar, boss_bar_rect = draw_boss_bar(COLUMN_WIDTH, 50, boss_sprites.sprite.health/boss_sprites.sprite.max_health, boss_sprites.sprite.shield/boss_sprites.sprite.max_shield, (COLUMN_WIDTH*2,SCREEN_HEIGHT-100))
            if boss_spawned:
                self.screen.blit(boss_bar, boss_bar_rect)

            explosions.draw(self.screen)
            bomb_explosion_sprites.draw(self.screen)
            chargeShot_Anim.draw(self.screen)
            player_bullet_sprites.draw(self.screen)
            player_bomb_sprites.draw(self.screen)
            enemy_bullet_sprites.draw(self.screen)
            items.draw(self.screen)
            if playerShip.invul_flag and invul_timer//6 % 2 == 0: ##allows visual feedback that the player is invulnerable
                player_sprites_invul.draw(self.screen)
            player_sprites.draw(self.screen)
            enemy_sprites.draw(self.screen)
            boss_sprites.draw(self.screen)

            c1 = self.screen.blit(column, ORIGIN)
            c2 = self.screen.blit(column, (SCREEN_WIDTH-COLUMN_WIDTH, 0))

            text = draw_text("Score: "+ str(player_score), WHITE)
            self.screen.blit(text,ORIGIN)

            self.screen.blit(inst_block, (0,text.get_rect().bottom))

            if DEBUG:
                debug_text = draw_text('FPS: '+str(round(self.clock.get_fps(), 2)), WHITE)
                debug_rect = self.screen.blit(debug_text, (0, SCREEN_HEIGHT - 100))
                self.screen.blit(debug_text, debug_rect)
                mission_timer_text = draw_text('Mission Time: '+ str(sec_running), WHITE)
                mission_timer_rect = self.screen.blit(mission_timer_text, (0, SCREEN_HEIGHT-150))
                self.screen.blit(mission_timer_text, mission_timer_rect)
            
            armor_bar, armor_bar_rect = draw_vertical_bar(RED, 50, SCREEN_HEIGHT-400, (playerShip.health/playerShip.max_health), (COLUMN_WIDTH*4 + 10,200))
            shield_bar, shield_bar_rect = draw_vertical_bar(BLUE, 50, SCREEN_HEIGHT-400, (playerShip.shield/playerShip.max_shield), (COLUMN_WIDTH*4 + 70,200))
            lives_left, lives_left_rect = draw_player_lives(player_lives, (COLUMN_WIDTH*4 + 10, 10))
            bombs_left, bombs_left_rect = draw_bombs_remaining(playerShip.bombs_remaining, (COLUMN_WIDTH*4 + 40, 100))

            self.screen.blit(lives_left, lives_left_rect)
            self.screen.blit(bombs_left, bombs_left_rect)
            self.screen.blit(armor_bar, armor_bar_rect)
            self.screen.blit(shield_bar, shield_bar_rect)
            
            pygame.display.flip()

            time_since_start += self.clock.tick_busy_loop(FRAMERATE)
            if playerShip.invul_flag:
                invul_timer -= 1
            regen_timer -= 1
            if regen_timer == 0:
                playerShip.regen()
                regen_timer = 6

            if playerShip.bomb_wait == True:
                bomb_timer -= 1
                if bomb_timer == 0:
                    playerShip.bomb_wait = False
                    bomb_timer = 120
        if next_level:
            self.level_complete()
        return player_lives, player_score, next_level, playerShip

    def pause_screen(self):
        '''Invokes the pause screen state.'''

        paused = True
        while paused:
            paused_text = draw_text('***PAUSED***', WHITE)
            paused_rect = paused_text.get_rect()
            paused_rect.center = SCREEN_CENTER 
            self.screen.blit(paused_text, paused_rect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_PAUSE or event.key == K_ESCAPE:
                        paused = False
                        pygame.time.wait(500)
                    if event.key == K_F12:
                            self.__fs_toggle = not self.__fs_toggle
                            if self.__fs_toggle:
                                pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                            else:
                                pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                    if event.key == K_p and DEBUG:
                        print(ASSET_MANAGER)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FRAMERATE)

    def ask_to_save(self, health, shield, weapon, bombs, score, lives, time_of_save):
        '''Invokes the "ask to save" state. Takes in all the parameters required to save the game via library's saveGame() method.'''

        text1 = draw_text('Do you want to save your progress?', WHITE, BLACK)
        text1_rect = text1.get_rect()
        text1_rect.center = SCREEN_CENTER

        button_yes, yes_rect = draw_button('YES', WHITE, BLACK, text1_rect.bottomleft)
        button_no, no_rect = draw_button('NO', WHITE, BLACK)
        button_cancel, cancel_rect = draw_button('CANCEL', WHITE, BLACK)
        no_rect.centerx, no_rect.y = text1_rect.centerx, text1_rect.bottom
        cancel_rect.topright = text1_rect.bottomright

        going = True
        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if yes_rect.collidepoint(event.pos):
                        saveGame([health, shield, weapon, bombs, score, lives, time_of_save, self.loader.levelNumber])
                        # print([health, shield, weapon, bombs, score, lives, time_of_save, self.loader.levelNumber])
                        return False, False
                    elif no_rect.collidepoint(event.pos):
                        return False, False              
                    elif cancel_rect.collidepoint(event.pos):
                        return True, True  

            self.screen.blit(text1, text1_rect)
            self.screen.blit(button_yes, yes_rect)
            self.screen.blit(button_no, no_rect)
            self.screen.blit(button_cancel, cancel_rect)

            pygame.display.update()

            self.clock.tick(FRAMERATE)
        
    def level_complete(self):
        '''Invokes visual transition from main() to main().'''

        going = True
        start_time = pygame.time.get_ticks()
        while going:
            victory_text = draw_text('Area cleared! Level Complete!', WHITE)
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
        '''Invokes the "you died!" state. Captures the spacebar to get back into the game.'''

        dead = True
        while dead:
            dead_text = draw_text('***YOUR SHIP WAS DESTROYED! Press Space to re-deploy!***', WHITE)
            dead_rect = dead_text.get_rect()
            dead_rect.center = SCREEN_CENTER 
            self.screen.blit(dead_text, dead_rect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        dead = False
                        pygame.time.wait(500)
                    if event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle
                        if self.__fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()
            self.clock.tick(FRAMERATE)
    
    def game_over(self, player_score):
        '''Invokes the game over screen. Mostly just a visual transition back to the main menu, since continuing is not an option.'''

        dead = True
        while dead:
            dead_text = draw_text('YOU\'VE BEEN DESTROYED! Country Orange has won!', WHITE)
            dead_rect = dead_text.get_rect()
            dead_rect.center = SCREEN_CENTER 
            dead_text2 = draw_text('Press Space to return to the main menu.', WHITE)
            dead_rect2 = dead_text2.get_rect()
            dead_rect2.centerx, dead_rect2.top = dead_rect.centerx, dead_rect.bottom  
            self.screen.blit(dead_text, dead_rect)
            self.screen.blit(dead_text2, dead_rect2)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        dead = False
                    if event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle 
                        if self.__fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()
            self.clock.tick(FRAMERATE)

    def add_to_hs(self, txt):
        '''Transitions to "add a high score" state.'''

        def blink(screen):
            for color in [BLACK, WHITE]:
                pygame.draw.circle(box, color, (x//2, int(y*0.7)), 7, 0)
                self.screen.blit(box, box_rect)
                pygame.display.flip()
                pygame.time.wait(300)
        def show_name(screen, name):
            pygame.draw.rect(box, WHITE, (50, 60, x-100, 20), 0)
            txt_surf = font.render(name, True, BLACK)
            txt_rect = txt_surf.get_rect(center=(x//2, int(y*0.7)))
            box.blit(txt_surf, txt_rect)
            self.screen.blit(box, box_rect)
            pygame.display.flip()
        font = pygame.font.Font(str(FONT_PATH.joinpath('OpenSans-Regular.ttf')), 16)
        x = 480
        y = 100
        # make box
        box = pygame.surface.Surface((x, y))
        box.fill(BLACK)
        box_rect = pygame.draw.rect(box, BLACK, (0, 0, x, y), 1)
        box_rect.center = SCREEN_CENTER
        txt_surf = font.render(txt, True, WHITE)
        txt_rect = txt_surf.get_rect(center=(x//2, int(y*0.3)))
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
        '''Main menu state. Allows use of the mouse and captures it for button clicky detection.'''

        pygame.mouse.set_visible(True) ##We need the mouse here.

        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath('nebula_red.png'))
        bg_size = bg.get_size()
        w, h = bg_size
        x = 0
        y = 0
        x1 = 0
        y1 = -h
        code_frame_counter = 120

        going = True
        konami = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a, K_RETURN]
        idsoft = [K_i, K_d, K_k, K_f, K_a, K_RETURN]
        in_code  = []
        konami_code_accepted = False
        idsoft_code_accepted = False

        title = draw_text('Day 0 - Another Raiden Clone', WHITE, None, 60, True)
        title_rect = title.get_rect()
        title_rect.centerx, title_rect.y = SCREEN_WIDTH//2, 100

        start_button, start_button_rect = draw_button('PLAY', WHITE, BLACK)
        load_button, load_button_rect = draw_button('LOAD GAME', WHITE, BLACK)
        quit_button, quit_button_rect = draw_button('QUIT', WHITE, BLACK)
        credits_button, credits_button_rect = draw_button('CREDITS', WHITE, BLACK)
        hs_list_button, hs_list_button_rect = draw_button('HALL OF FAME', WHITE, BLACK)


        start_button_rect.center = SCREEN_CENTER
        load_button_rect.centerx, load_button_rect.top = start_button_rect.centerx, start_button_rect.bottom+10
        quit_button_rect.centerx, quit_button_rect.top = load_button_rect.centerx, load_button_rect.bottom+10
        credits_button_rect.centerx, credits_button_rect.top = quit_button_rect.centerx, quit_button_rect.bottom+10
        hs_list_button_rect.centerx, hs_list_button_rect.top = credits_button_rect.centerx, credits_button_rect.bottom+10

        while going:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key == K_SPACE:
                        gui.level_loop(1, konami_code_accepted, idsoft_code_accepted)
                        in_code = []
                        konami_code_accepted = False
                        idsoft_code_accepted = False
                    elif event.key == K_s:
                        gui.high_scores()
                    elif event.key == K_c:
                        gui.credits()
                    elif event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle 
                        if self.__fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])
                    elif event.key == K_RETURN:
                        in_code.append(K_RETURN)
                        if in_code == konami:
                            konami_code_accepted = True
                        if in_code == idsoft:
                            idsoft_code_accepted = True
                        in_code = []
                    else:
                        in_code.append(event.key)
                elif event.type == MOUSEMOTION:
                    if start_button_rect.collidepoint(event.pos):
                        start_button, start_button_rect = draw_button('PLAY', BLACK, YELLOW, start_button_rect.topleft, True)
                    elif load_button_rect.collidepoint(event.pos):
                        load_button, load_button_rect = draw_button('LOAD GAME', BLACK, YELLOW, load_button_rect.topleft, True)
                    elif quit_button_rect.collidepoint(event.pos):
                        quit_button, quit_button_rect = draw_button('QUIT', BLACK, YELLOW, quit_button_rect.topleft, True)
                    elif credits_button_rect.collidepoint(event.pos):
                        credits_button, credits_button_rect = draw_button('CREDITS', BLACK, YELLOW, credits_button_rect.topleft, True)
                    elif hs_list_button_rect.collidepoint(event.pos):
                        hs_list_button, hs_list_button_rect = draw_button('HALL OF FAME', BLACK, YELLOW, hs_list_button_rect.topleft, True)
                    else:
                        start_button, start_button_rect = draw_button('PLAY', WHITE, BLACK, start_button_rect.topleft)
                        load_button, load_button_rect = draw_button('LOAD GAME', WHITE, BLACK, load_button_rect.topleft)
                        quit_button, quit_button_rect = draw_button('QUIT', WHITE, BLACK, quit_button_rect.topleft)
                        credits_button, credits_button_rect = draw_button('CREDITS', WHITE, BLACK, credits_button_rect.topleft)
                        hs_list_button, hs_list_button_rect = draw_button('HALL OF FAME', WHITE, BLACK, hs_list_button_rect.topleft)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  ##1 is the Left Button
                    if start_button_rect.collidepoint(event.pos):
                        gui.level_loop(1, konami_code_accepted, idsoft_code_accepted)
                        in_code = []
                        konami_code_accepted = False
                        idsoft_code_accepted = False
                    elif load_button_rect.collidepoint(event.pos):
                        gui.level_loop(toLoad=True)
                    elif quit_button_rect.collidepoint(event.pos):
                        going = False
                    elif credits_button_rect.collidepoint(event.pos):
                        gui.credits()
                    elif hs_list_button_rect.collidepoint(event.pos):
                        gui.high_scores()


                        
                       
            y1 += 1
            y += 1
            self.screen.blit(bg,(x,y))
            self.screen.blit(bg,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h

            text5 = draw_text('CODE ACCEPTED. ENJOY CHEATING WITH ALL THOSE LIVES!', WHITE)
            text_rect5 = text5.get_rect()
            text_rect5.centerx, text_rect5.bottom = self.screen_rect.centerx, SCREEN_HEIGHT-100

            text6 = draw_text('CODE ACCEPTED. ENJOY YOUR NEW WEAPONS!', WHITE)
            text_rect6 = text6.get_rect()
            text_rect6.centerx, text_rect6.top = text_rect5.centerx, text_rect5.bottom

            self.screen.blit(title, title_rect)
            self.screen.blit(start_button, start_button_rect)
            self.screen.blit(load_button, load_button_rect)
            self.screen.blit(quit_button, quit_button_rect)
            self.screen.blit(credits_button, credits_button_rect)
            self.screen.blit(hs_list_button, hs_list_button_rect)

            if konami_code_accepted:
                self.screen.blit(text5, text_rect5)
            if idsoft_code_accepted:
                self.screen.blit(text6, text_rect6)

            pygame.display.flip()

            self.clock.tick(FRAMERATE)
        
        pygame.quit()

    def credits(self):
        '''Transition to the credits crawl.'''

        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath('nebula.jpg'))
        with open(EVENT_SCROLL_PATH.joinpath('credits.asset')) as infile:
            credit_list = infile.readlines()

        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False 

            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in credit_list:
                line = line.strip('\n')
                text = draw_text(line, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0: ###because of the for loop, this is guaranteed to be the last line of text
                going = False
            self.clock.tick(FRAMERATE)

    def high_scores(self):
        '''Transition to the high score crawl.'''

        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath('nebula.jpg'))
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        hs_list = str(self.hs_list).split(sep='\n')

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False 


            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in hs_list:
                text = draw_text(line, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (x,y)
                y += 50
                self.screen.blit(text, text_rect)

            count += 1
            pygame.display.update()

            if text_rect.bottom < 0:
                going = False
            self.clock.tick(FRAMERATE)

    def level_loop(self, level=1, cheat_lives=False, cheat_weaps=False, toLoad=False):
        '''Looper that ensures everything is set up for main(), while also allowing a loaded file to work correctly.'''

        pygame.mouse.set_visible(False) ##turn the mouse back off

        if not toLoad:
            self.loader = levelLoader.LevelLoader(level)
            curr_score = 0
            curr_time = 0
            playerShip = None

            if cheat_lives:
                curr_lives = 100
            else:
                curr_lives = 3

            if cheat_weaps:
                playerShip = Entity.Player('master_lazer',MISC_SPRITES_PATH.joinpath('SweetShip.png'),"arrows") 

        else:
            pickled_goods = loadGame()
            ##[health, shield, weapon, bombs, score, lives, time_of_save, self.loader.levelNumber]
            playerShip = Entity.Player(pickled_goods[2], MISC_SPRITES_PATH.joinpath('SweetShip.png'), 'arrows')
            playerShip.health = pickled_goods[0]
            playerShip.shield = pickled_goods[1]
            playerShip.bombs_remaining = pickled_goods[3]
            curr_score = pickled_goods[4]
            curr_lives = pickled_goods[5]
            curr_time = pickled_goods[6]
            self.loader = levelLoader.LevelLoader(pickled_goods[7])


        still_playing = True

        while still_playing:
            curr_lives, curr_score, next_level, playerShip = self.main(curr_lives, curr_score, playerShip, curr_time)
            is_next_level = self.loader.nextLevel()
            if not next_level:
                still_playing = False
            elif not is_next_level:
                still_playing = False
                self.victory()
                if self.hs_list.belongsOnList(curr_score):
                    name = self.add_to_hs('You set a new high score! Enter your initials!')
                    self.hs_list.add(name, curr_score)
                    self.hs_list.writeToFile(EVENT_SCROLL_PATH.joinpath('highscores.asset'))
        self.loader = levelLoader.LevelLoader()
        pygame.mouse.set_visible(True)
   
    def victory(self):
        '''Transition to end of game "you win!" state.'''

        ##Background setup
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        bg, bg_rect = ASSET_MANAGER.getAsset(BACKGROUND_PATH.joinpath('nebula_blue.png'))
        background.fill(BLACK)
        background.blit(bg, ORIGIN)

        story_scroll = load_text(EVENT_SCROLL_PATH.joinpath('ending.asset'))

        going = True
        count = 0

        while going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        going = False 
                    if event.key == K_F12:
                        self.__fs_toggle = not self.__fs_toggle 
                        if self.__fs_toggle:
                            pygame.display.set_mode(WINDOW_OPTIONS_FULLSCREEN[0], WINDOW_OPTIONS_FULLSCREEN[1])
                        else:
                            pygame.display.set_mode(WINDOW_OPTIONS_WINDOWED[0], WINDOW_OPTIONS_WINDOWED[1])

            self.screen.blit(background, ORIGIN)

            x = SCREEN_WIDTH/2
            y = SCREEN_HEIGHT - count

            for line in story_scroll:
                line = line.strip('\n')
                text = draw_text(line, WHITE)
                text_rect = text.get_rect()
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
    


