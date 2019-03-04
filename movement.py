'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''
import copy
import math

import pygame

from library import *


class Move(object):#REMOVE behaviorArray, SpeedArray, and AngelArray, Replace exitScreen with  "times to repeat"
    def __init__(self, moveCountArray=[800], vectorAray=[["x",3,0]], rotationArray=[], repeat=3):
        '''The vector Array contains all the information needed for movment over frames'''
        

        self.save=[]#save to reinitialize arrays to loop movements
        self.save.append(copy.deepcopy(moveCountArray))
        self.save.append(copy.deepcopy(vectorAray))
        self.save.append(copy.deepcopy(rotationArray))

        
       
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.currMove = 0 
       
        self.rotations = rotationArray
        self.currRotation = 0
        self.repeat = repeat
       
       #NEW STUFF HERE
        self.currVector = 0 # [#frames, entityAcceleration, entitySpeed, entityAngle]
        self.vectors = vectorAray # contains a list frames to go through for each speed accerlation and angle change
        

    def __vector__ (self,spriteObject):
        '''do all the vector math here'''
        
        changeAccel = self.currVector[0]
        changeSpeed = self.currVector[1]
        changeAngel = self.currVector[2]
        
        #speed v= Dv + a[frame]
        
        #check for x, will update sprite values if not x.
        if changeAccel != "x":
            
            spriteObject.acceleration = changeAccel
        if changeAngel != "x": #when angle changes, that speed diff needs to be added to current speed
            spriteObject.angle = changeAngel
        if changeSpeed != "x":
            
            spriteObject.speed= changeSpeed #adjusts speedX, and speedY appropriately on object
       
        spriteObject.updateSpeed() #accelerates object by increasing speedX and speedY by adding angled accel
        
        spriteObject.move(int(spriteObject.speedX),int(spriteObject.speedY))

        return spriteObject

    

    def __updateCurrMove__(self): 
        '''updates currMove, as well as currBehavior and currSpeed'''
        if len(self.moveCounts)==0 and self.currMove==0:
            return True # this means there are no more moves to be made, so exitscreen will be checked or movement reset
        if self.currMove <= 0:
            self.currMove = self.moveCounts.pop(0)
            if len(self.vectors) > 0:
                self.currVector = self.vectors.pop(0)
            if len(self.rotations)>0:
                self.currRotation = self.rotations.pop(0)
        
        else: self.currMove -=1 #decrments 1 frame from move count
        return False
        
    def update(self,spriteObject):
       
        if self.currRotation != spriteObject.rotation:
            image, rect = load_image(spriteObject.imgFile) 
            spriteObject.image,spriteObject.rect = self.rot_center(image, spriteObject.rect, self.currAngle)
            spriteObject.rotation = self.currRotation

        if self.__updateCurrMove__(): # will initialize currSpeed, currMove, and currBehavior, and return True if no more moves left
            if self.repeat>0: #will update reset the bahavior
                self.moveCounts = copy.deepcopy(self.save[0])
                self.vectors = copy.deepcopy(self.save[1])
                self.rotations = copy.deepcopy(self.save[2])
                self.__updateCurrMove__()
            else: #will begin off screen behavior
                self.moveCounts = [1,800]
                self.vectors=[[2,0,0], ["x","x","x"]]#sets acceleration to 2 and exits screen
                self.__updateCurrMove__()
            
            self.repeat -=1
        
        updatedObject = self.__vector__(spriteObject)
        
        return updatedObject

    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect



