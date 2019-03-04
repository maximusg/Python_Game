import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
import weapon
import math
from library import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

class entity2(pygame.sprite.DirtySprite):
    def __init__(self, origin=[0,0], imageFile=None, area=None, acceleration=0,speed=0, angle=0, health=1):
        super().__init__()
        self.health = health
        self.screen = pygame.display.get_surface()
        self.speedX = math.sin(math.radians(angle))*speed
        self.speedY = math.cos(math.radians(angle))*speed
        self.speed = speed
        self.angle = angle
        self.rotation = 0
        self.acceleration = acceleration
        self.imageFile = imageFile
        self.image=None
        self.rect=None
        
        self.area=None
        if area==None: #defualts to Enemies set area... might want to change
            self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
        else:
            self.area = area

        #loading picture    
        
        if imageFile!=None:
            self.image, self.rect = load_image(imageFile)
        else:#if no image give creates a 20X20 red square.
            self.image = pygame.Surface([20, 20])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
        self.rect.x = origin[0]
        self.rect.y = origin[1]
        


    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, value):
        if not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid int for health.')
        self.__health = value

    @property
    def angle(self):
        return self.__angle
    
    @angle.setter
    def angle(self, value):#speed comes before angel so need to check if it exists like speed chesk for angle
        if not isinstance(value, int) and not isinstance(value,float):
            raise RuntimeError(value + ' is not a valid int for angle.')
        value = value%360
        self.speedX = math.sin(math.radians(value))*self.speed
        self.speedY = math.cos(math.radians(value))*self.speed

        self.__angle = value


    @property
    def rotation(self):
        return self.__rotation
    
    @rotation.setter
    def rotation(self, value):#speed comes before angel so need to check if it exists like speed chesk for angle
        if not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid int for angle.')
        value = value%360

        self.__rotation = value

    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self, value):
        if not isinstance(value, int) and not isinstance(value,float):
            raise RuntimeError(value + ' is not a valid int for speed.')
        try :
            self.angle #checks for the first case when angle is being contructed
        except: 
            self.__speed = value
        else:
            self.speedX = math.sin(math.radians(self.angle))*value
            self.speedY = math.cos(math.radians(self.angle))*value
            self.__speed = value

    @property
    def acceleration(self):
        return self.__acceleration
    
    @acceleration.setter
    def acceleration(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid float for acceleration.')
        self.__acceleration = value

    def updateSpeed(self):
        self.speedX += math.sin(math.radians(self.angle))*self.acceleration 
        self.speedY += math.cos(math.radians(self.angle))*self.acceleration
    
    def move(self, x, y):#keeps object from going past the  sides
        if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
            self.rect.left = self.area.left
            self.speedX = -self.speedX
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
            self.speedX = -self.speedX
        else:
            self.rect = self.rect.move((x, y))
        self.dirty = 1
            
            



