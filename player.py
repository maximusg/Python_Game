import entity2
import pygame
import bullet
import weapon
from library import *



class player(entity2.entity2):
    def __init__(self, init_wep, imgFile, scheme):
        super().__init__()
        self.weapon = weapon.Weapon(init_wep)
        self.control_scheme = scheme ##placeholder
        self.point_total = 0
        self.image, self.rect = load_image(imgFile, -1)
        self.area = self.screen.get_rect()
        self.rect.topleft = 500,600
        self.speed = 10
        self.bullet_count = 0

    def move(self, new_x, new_y):
        #if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
        #    self.rect.left = self.area.left
        #elif self.rect.right > self.area.right:
        #    self.rect.right = self.area.right
        #elif self.rect.top < self.area.top:
        #    self.rect.top = self.area.top
        #elif self.rect.bottom > self.area.bottom:
        #    self.rect.bottom = self.area.bottom
        #else:
        #    self.rect = self.rect.move((new_x, new_y))
        if check_bounds(self.rect, self.area):
            self.rect = self.rect.move((new_x, new_y))
        self.dirty = 1
    
    def update(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom

    def fire(self):
        return bullet.bullet(self.rect.centerx, self.rect.top, 5, self.weapon.weapon_image)
    
    def control(self, FRAMERATE):
        keys = pygame.key.get_pressed()
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
            
            if keys[pygame.K_SPACE]:
                if self.bullet_count % (int(FRAMERATE/self.weapon.rof)) == 0:
                    addBullet=True
                self.bullet_count += 1
            else:
                self.bullet_count = 0
        return addBullet