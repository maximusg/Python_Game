import entity2
import explosion
import bullet
import math
from library import *
from levelLibrary import *
import random

class BossSprite(entity2.entity2):
    def __init__(self, origin, path_to_img):
        super().__init__()
        self.image, self.rect = load_image(path_to_img)
        self.shield_gen_loc = (220, 30)
        self.rect.x = origin[0]
        self.rect.y = origin[1]
        self.launchers = ((250,95),(150,95),(50,95))

        self.point_value = 50000
        self.max_health = 150
        self.health = self.max_health
        self.max_shield = 100
        self.shield = self.max_shield
        self.regen_counter = 90

        self.phase = 1
        self.phase_counter = 300

        self.layer = 1
        self.dirty = 2
        self.visible = 1

    def update(self, player_center):
        self.move()
        self.regen()

        explosion_list = []
        bullet_list = []

        ##set up explosions
        if self.shield == 0:
            if random.random() < 0.05:
                explosion_list.append(explosion.ExplosionSprite(self.rect.left + self.shield_gen_loc[0]+random.randint(-2,2), self.rect.top + self.shield_gen_loc[1]+random.randint(-2,2), 'up'))
        
        if 0.25 < self.health / self.max_health <= 0.5:
            if random.random() < 0.05:
                explosion_list.append(explosion.ExplosionSprite(random.randint(self.rect.left, self.rect.right), random.randint(self.rect.top, self.rect.bottom), 'up'))
        if 0 <= self.health / self.max_health <= 0.25:
            if random.random() < 0.15:
                explosion_list.append(explosion.ExplosionSprite(random.randint(self.rect.left, self.rect.right), random.randint(self.rect.top, self.rect.bottom), 'up'))
        
        #set up bullets
        if self.phase == 1:
            if random.random() < 0.05:
                bullet_list.append(bullet.bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
                bullet_list.append(bullet.bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
                bullet_list.append(bullet.bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
            self.phase_counter -= 1
            if self.phase_counter == 0:
                self.phase_counter = 600
                self.phase = 2
        elif self.phase == 2:
            if random.random() < 0.1:
                if player_center[1] > self.rect.bottom:
                    delta_x = (self.rect.x+self.launchers[0][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', angle, 'vector'))

                    delta_x = (self.rect.x+self.launchers[1][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', angle, 'vector'))

                    delta_x = (self.rect.x+self.launchers[2][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', angle, 'vector'))
                else:
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
                    bullet_list.append(bullet.bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', random.randint(-45,45),'vector'))
            self.phase_counter -= 1
        
        return explosion_list, bullet_list
        

    def move(self):
        if self.phase == 1:
            if self.rect.y < 300:
                self.rect = self.rect.move(0,3)
            else:
                self.rect = self.rect.move(random.randint(-2,2), random.randint(-2,2))
        elif self.phase == 2:
            if self.rect.y > 100:
                self.rect = self.rect.move(random.randint(-5,5),-5)
            else:
                self.rect = self.rect.move(random.randint(-2,2),0)


    def regen(self):
        if self.regen_counter == 0:
            if 0 < self.shield < self.max_shield:
                self.shield += 1
                self.regen_counter = 90
        else:
            self.regen_counter -= 1
            

    def take_damage(self, value):
        if self.shield > 0:
            self.shield -= value
        else:
            self.health -= value
        if self.health <= 0:
            self.visible = 0
        

        