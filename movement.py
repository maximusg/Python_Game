'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''
import copy
import math

import pygame

from library import *


class Move(object):
    def __init__(self, behaviorArray=["down"], moveCountArray=[800], speedArray=[10], angelArray=[0], vectorAray=[["x","x","x"]], rotationArray=[], exitscreen=True):
        '''The vector Array contains all the information needed for movment over frames'''
        self.behaveDic = {
            "down": self.__down__, 
            "up":self.__up__, 
            "left":self.__left__, 
            "right":self.__right__, 
            "stop": self.__stop__,
            "northWest": self.__northWest__,
            "northNorthWest": self.__northNorthWest__,
            "northEast": self.__northEast__,
            "northNorthEast": self.__northNorthEast__,
            "southWest": self.__southWest__, #typo, change to southWest
            "southEast": self.__southEast__,
            "vector": self.__vector__

            }

        self.save=[]#save to reinitialize arrays to loop movements
        if exitscreen==False:
            self.save.append(copy.deepcopy(behaviorArray))
            self.save.append(copy.deepcopy(moveCountArray))
            self.save.append(copy.deepcopy(speedArray))
            self.save.append(copy.deepcopy(angelArray)) 
            self.save.append(copy.deepcopy(vectorAray))
            self.save.append(copy.deepcopy(rotationArray))

        self.behaviors = behaviorArray #list of methods to run from the behaveDic
        self.currBehavior = None
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.currMove = 0 
        self.speeds = speedArray #used to change speeds between behaviors, if no more speeds left, defaults to last speed given
        self.currSpeed = 0 
        self.angles = angelArray
        self.currAngle=0
        self.angleBool = False
        self.rotations = rotationArray
        self.currRotation = 0
       
       #NEW STUFF HERE

       
        self.currVector = 0 # [#frames, entityAcceleration, entitySpeed, entityAngle]
        self.vectors = vectorAray # contains a list frames to go through for each speed accerlation and angle change

        
        

        
        self.exitsceen = exitscreen #if true, this behaivor will result in enemy moving down and off screen after executing movements to be deleted else enemy will stay put




    def __up__(self,spriteObject):
        return spriteObject.move(0,-self.currSpeed)

    def __down__(self,spriteObject):
        return spriteObject.move(0,self.currSpeed)

    def __left__(self,spriteObject):
        
        return spriteObject.move(-self.currSpeed,0)

    def __right__(self,spriteObject):
        return spriteObject.move(self.currSpeed,0)

    def __stop__(self,spriteObject):
        return spriteObject.move(0,0)
    
    def __northWest__(self,spriteObject):
        return spriteObject.move(-self.currSpeed,-self.currSpeed)

    def __northNorthWest__(self,spriteObject):
        return spriteObject.move(-self.currSpeed,-self.currSpeed*2)
    
    def __northEast__(self,spriteObject):
        return spriteObject.move(self.currSpeed,-self.currSpeed)

    def __northNorthEast__(self,spriteObject):
        return spriteObject.move(self.currSpeed,-self.currSpeed*2)

    def __southEast__(self,spriteObject):
        return spriteObject.move(self.currSpeed,self.currSpeed)

    def __southWest__(self,spriteObject):
        return spriteObject.move(-self.currSpeed,self.currSpeed)

    def __vector__ (self,spriteObject):
        '''do all the vector math here'''
        changeAccel = self.currVector[0]
        changeSpeed = self.currVector[1]
        changeAngel = self.currVector[2]
        
        #speed v= Dv + a[frame]
        #so accel will speed up speed by the number of frames given unless it is 0
        #check for x, will update sprite values if not x.
        if changeAccel != "x":
            spriteObject.acceleration = changeAccel
        if changeAngel != "x": #when angle changes, that speed diff needs to be added to current speed
            spriteObject.angle = changeAngel
        if changeSpeed != "x":
            spriteObject.speed= changeSpeed
       
        # print(spriteObject.acceleration, spriteObject.angle, spriteObject.speed, spriteObject.speedX, spriteObject.speedY)

        spriteObject.updateSpeed() #accelerates object
    
        return spriteObject.move(int(spriteObject.speedX),int(spriteObject.speedY))

    

    def __updateCurrMove__(self): 
        '''updates currMove, as well as currBehavior and currSpeed'''
        if len(self.moveCounts)==0 and self.currMove==0:
            return True # this means there are no more moves to be made, so exitscreen will be checked or movement reset
        if self.currMove <= 0:
            self.currMove = self.moveCounts.pop(0)
            if len(self.behaviors)>0:
                self.currBehavior = self.behaviors.pop(0)
            if len(self.speeds) >0:
                self.currSpeed = self.speeds.pop(0)
            if len(self.angles) > 0:
                self.currAngle = self.angles.pop(0)
            if len(self.vectors) > 0:
                self.currVector = self.vectors.pop(0)
            if len(self.rotations)>0:
                self.currRotation = self.rotations.pop(0)
                
        else: self.currMove -=1 #decrments 1 frame from move count
        return False
        
    def update(self,spriteObject):
       
        if self.currRotation != spriteObject.rotation:
            image, rect = load_image(spriteObject.imgFile) 
            # sav = spriteObject.angle
            # if spriteObject.angle != 0:
            #     image, spriteObject.rect = self.rot_center(image, spriteObject.rect, -spriteObject.angle)
            spriteObject.image,spriteObject.rect = self.rot_center(image, spriteObject.rect, self.currAngle)
            spriteObject.rotation = self.currRotation

        if self.__updateCurrMove__(): # will initialize currSpeed, currMove, and currBehavior, and return True if no more moves left
            if not self.exitsceen: #will update reset the bahavior
                self.behaviors = copy.deepcopy(self.save[0]) 
                self.moveCounts = copy.deepcopy(self.save[1])
                self.speeds = copy.deepcopy(self.save[2]) 
                self.angles = copy.deepcopy(self.save[3]) 
                self.vectors = copy.deepcopy(self.save[4])
                self.rotations = copy.deepcopy(self.save[5])
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
