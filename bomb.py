'''
Purpose:

key reserved for firing the main weapon.

A bomb will slowly move forward before exploding after a set time.
The explosion will cause a circle with a radius that grows up to a certain point, that will deal damage to all enemies
that it collides with.

The player should have a set number of bombs that can be collected. However, even if a player
has multiple bombs, there should be a short duration after a player launches the first bomb that they will not be able
to launch another bomb.

'''

import entity2
import pygame.mask
import movement
from library import *
from pathlib import Path

cwd = Path.cwd()
bomb_sounds = cwd.joinpath('resources', 'sound_effects', 'bomb_sounds')

class bomb(entity2.entity2):
    def __init__(self, origin_x, origin_y, speed, path_to_img, angle=0, behavior='up'):
        location =(origin_x, origin_y)
        area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
        super().__init__(origin=location, imageFile=path_to_img, area=area, speed=speed, angle=angle)
        # self.speed = speed
        # self.image, self.rect = load_image(path_to_img)
        # self.image = self.image.convert()
        # self.imgFile = path_to_img
        # self.rect.centerx, self.rect.top = origin_x, origin_y
        self.off_screen = False
        self.dirty = 1
        self.mask = pygame.mask.from_surface(self.image)
        # self.angle = angle

        self.sound = load_sound(str(bomb_sounds.joinpath('bomb_drop.ogg')))


        # self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
        # self.rect.x = origin_x
        # self.rect.y = origin_y


        #self.is_bomb = is_bomb
        self.bomb_timer = 100
        self.bomb_explode = False
        self.centerx = self.rect.x
        self.centery = self.rect.y


        self.behaveDic = {
            "bomb": self.__bomb__,
            "upSlow": self.__upSlow__

        }

        self.movement = self.behaveDic[behavior]()

    # def move(self):
    # 	self.rect = self.rect.move(self.angle,-self.speed)
    # 	self.dirty = 1
    def play_sound(self):
        self.sound.play()

    # def move(self, x, y):

    #     self.rect = self.rect.move((x, y))
    #     self.dirty = 1

    def update(self):
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.right > SCREEN_WIDTH - COLUMN_WIDTH or self.rect.left < COLUMN_WIDTH:  # checks if the rect is out of bounds, and if so, it is no longer visible, meaning it should be deleted by GUI
            self.visible = 0
            self.dirty = 1

        #new movement after bomb slows down to a threshold of speed 3. upSlow moves the bomb up slowly forever
        if self.speed <= 3:
            self.movement = self.__upSlow__()

        self.bomb_timer -= 1
        if self.bomb_timer <= 0 and self.visible == 1:
            self.visible = 0
            #self.is_bomb = False
            #print('BOOM')
            self.bomb_explode = True
            self.centerx= self.rect.x
            self.centery = self.rect.y
        # self.image, self.rect = load_image('resources/misc_sprites/explosion1.png')
        
        self.movement.update(self)
        
        


    # if not (COLUMN_WIDTH <= self.rect.right and self.rect.left <= SCREEN_WIDTH-COLUMN_WIDTH):
    # 	self.visible = 0
    # if not (0 <= self.rect.top <= SCREEN_HEIGHT):
    # 	self.visible = 0


    def __upSlow__(self):
        moveCountArray = [3000]
        vectorArray = [[0, 2, 180]]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=99)


    def __bomb__(self):
        moveCountArray = [1,300]
        vectorArray = [[0, 15, 180,],[-.3, "x", 180]]


        #stopVector = []

        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=99)
