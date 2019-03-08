import entity2
import pygame
import bullet
import weapon
import explosion
from library import *
import random



class player(entity2.entity2):
    def __init__(self, init_wep, imgFile, scheme, init_bomb = 'bomb'):
        super().__init__()
        self.weapon = weapon.Weapon(init_wep)

        self.bomb = weapon.Weapon(init_bomb)
        self.bombs_remaining = 3
        self.bomb_wait = False
        self.drop_bomb_flag = False
        self.curr_bomb = None

        self.control_scheme = scheme ##placeholder
        self.point_total = 0
        self.max_health = 40
        self.health = 40
        self.max_shield = 100
        self.shield = 100
        self.image, self.rect = load_image(imgFile, -1)
        self.invul_flag = False

        self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)

        self.rect.center = self.area.centerx, SCREEN_HEIGHT-100
        self.speed = 10
        self.bullet_count = 0
        self.dirty = 2

    def take_damage(self, value):
        if self.shield > 0:
            self.shield -= value*2
            if self.shield < 0:
                self.health -= int(abs(self.shield*0.5))
                self.shield = 0
        else:
            self.health -= value

    def regen(self):
        self.shield += 1
        if self.shield > self.max_shield:
            self.shield = 100

    def move(self, new_x, new_y):
        if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
            self.rect.left = self.area.left
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
        elif self.rect.top < self.area.top:
            self.rect.top = self.area.top
        elif self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom
        else:
            self.rect = self.rect.move((new_x, new_y))
        #self.dirty = 1

    def fire(self):
        origin_x = (self.rect.left + self.rect.right) / 2
        origin_y = self.rect.top

        return self.weapon.weapon_func(origin_x, origin_y)
        #return bullet.bullet(origin_x, origin_y, 5, self.weapon.weapon_image)

    def drop_bomb(self):
        origin_x = (self.rect.left + self.rect.right) / 2
        origin_y = self.rect.top
        self.drop_bomb_flag = True
        self.bomb_wait = True
        #self.curr_bomb = True

        return self.bomb.weapon_func(origin_x, origin_y)
    
    def control(self, keys, FRAMERATE):
        addBullet=False
        if self.control_scheme=="arrows":
            if keys[pygame.K_UP]:
                self.move(0,-self.speed)
            if keys[pygame.K_DOWN]:
                self.move(0,self.speed)
            if keys[pygame.K_LEFT]:
                self.move(-self.speed, 0)
            if keys[pygame.K_RIGHT]:
                self.move(self.speed, 0)
            ##this if/else statement must stay together
            if keys[pygame.K_SPACE]:
                if self.bullet_count % (int(FRAMERATE/self.weapon.rof)) == 0:
                    addBullet=True
                self.bullet_count += 1
            else:
                self.bullet_count = 0

            ##this if/else statement must stay together
            if keys[pygame.K_b]:
                if self.bomb_wait == False and self.bombs_remaining > 0:
                    self.drop_bomb()
                    self.bombs_remaining -= 1
            ##end if/else    
            if DEBUG:        
                if keys[pygame.K_1]:

                    self.weapon = weapon.Weapon('waveBeam')
                if keys[pygame.K_2]:

                    self.weapon = weapon.Weapon('spitfire2')

                if keys[pygame.K_3]:
                    self.weapon = weapon.Weapon('spitfire3')


        return addBullet

    def update(self):
        if 0.75 < self.health / self.max_health <= 0.9:
            if random.random() < 0.01:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        elif 0.3 < self.health / self.max_health <= 0.75:
            if random.random() < 0.05:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        elif 0 <= self.health / self.max_health <= 0.3:
            if random.random() < 0.15:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        else:
            return None