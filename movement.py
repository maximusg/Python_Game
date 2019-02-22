'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''
import copy
import pygame
from library import *
import math
import pymunk

class Move(object):
    def __init__(self):
        
        
    def update(self,spriteObject):
        spriteObject.speedX  = math.sin(math.radians(changeAngel))*changeSpeed # get speed if there is angle change
        spriteObject.speedY =  math.cos(math.radians(changeAngel))*changeSpeed
        if self.angleBool: #just to save cycles, prevent loading picture if uncessary
            if self.currAngle != spriteObject.angle:
                image, rect = load_image(spriteObject.imgFile) 
                # sav = spriteObject.angle
                # if spriteObject.angle != 0:
                #     image, spriteObject.rect = self.rot_center(image, spriteObject.rect, -spriteObject.angle)
                spriteObject.image,spriteObject.rect = self.rot_center(image, spriteObject.rect, self.currAngle)
                
                spriteObject.angle = self.currAngle

        if self.__updateCurrMove__(): # will initialize currSpeed, currMove, and currBehavior, and return True if no more moves left
            if not self.exitsceen: #will update reset the bahavior
                self.behaviors = copy.deepcopy(self.save[0]) 
                self.moveCounts = copy.deepcopy(self.save[1])
                self.speeds = copy.deepcopy(self.save[2]) 
                self.angles = copy.deepcopy(self.save[3]) 
                self.vectors = copy.deepcopy(self.save[4])
                self.__updateCurrMove__()
            else: #will begin off screen behavior
                self.behaviors = ["down"]
                self.moveCounts = [800]
                self.speeds = [10]
                self.__updateCurrMove__()

        #spriteObject.move(0,1) #keeps ships constantly moving down
        updatedObject = self.behaveDic[self.currBehavior](spriteObject)
        
        return updatedObject

    # def rot_center(self, image, angle):
    #     """rotate an image while keeping its center and size"""
    #     orig_rect = image.get_rect()
    #     rot_image = pygame.transform.rotate(image, angle)
    #     rot_rect = orig_rect.copy()
    #     rot_rect.center = rot_image.get_rect().center
    #     rot_image = rot_image.subsurface(rot_rect).copy()
    #     return rot_image
    
    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

    # def upAndDown(self):
    #     if self.reversed == False:
    #             self.rect = self.rect.move(self.angle,-self.speed)
    #             self.move_counter += 1

    #             if self.move_counter == self.move_limit:
    #                 self.reversed = True

    #     elif self.reversed == True:

    #         self.rect = self.rect.move(self.angle, self.speed)
    #         self.move_counter -= 1

    #         if self.move_counter == 0:
    #             self.reversed = False


