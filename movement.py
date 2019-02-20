'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''
import copy
import pygame
from library import *
import math

class Move(object):
    def __init__(self, behaviorArray=["down"], moveCountArray=[800], speedArray=[10], angelArray=[0], vectorAray=[["x","x","x"]], exitscreen=True):
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

        self.behaviors = behaviorArray #list of methods to run from the behaveDic
        self.currBehavior = None
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.currMove = 0 
        self.speeds = speedArray #used to change speeds between behaviors, if no more speeds left, defaults to last speed given
        self.currSpeed = 0 
        self.angles = angelArray
        self.currAngle=0
        self.angleBool = False
       
       #NEW STUFF HERE

       
        self.currVector = 0 # [#frames, entityAcceleration, entitySpeed, entityAngle]
        self.vectors = vectorAray # contains a list frames to go through for each speed accerlation and angle change

        if len(angelArray) != 0:
            if len(angelArray)>0  or angelArray[0]>0: 
                self.angleBool=True
            else:  
                self.angleBool=False
        

        
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
        changeAngel = changeAngel%360 # converts change angle to positive direction
        #speed v= Dv + a[frame]
        #so accel will speed up speed by the number of frames given unless it is 0
        
        #  #check for X's ensure the correct values placed in all locations
        if changeAccel != "x":
            spriteObject.acceleration = changeAccel
        if changeSpeed != "x" and changeAngel != "x":
            spriteObject.speedX  = math.sin(math.radians(changeAngel))*changeSpeed # get speed if there is angle change
            spriteObject.speedY =  math.cos(math.radians(changeAngel))*changeSpeed
        if changeAngel != "x": #when angle changes, that speed diff needs to be added to current speed
            spriteObject.angle = changeAngel


        

        aX = math.sin(math.radians(changeAngel))*spriteObject.acceleration # get speed if there is angle change
        aY = math.cos(math.radians(changeAngel))*spriteObject.acceleration
        
       

        spriteObject.speedX += aX
        spriteObject.speedY += aY
        
    
        # spriteObject.angle = math.degrees(math.atan2(sY,sX))
        
        # spriteObject.speed = math.sqrt(sX**2+sY**2) 
        
        
        return spriteObject.move(int(spriteObject.speedX),int(spriteObject.speedY))




       
        #     newXSpeed = math.sin(math.radians(spriteObject.angle))*spriteObject.speed + oldX # get speed if there is angle change
        #     newYSpeed = math.cos(math.radians(spriteObject.angle))*spriteObject.speed + oldX
        
        # newXSpeed = newXSpeed - oldX
        
        
        
        # #add acceleration
        # print("Yspeed ", newYSpeed, math.cos(math.radians(spriteObject.angle))*spriteObject.acceleration)
        
        # print("Yspeed ", newYSpeed)
        # spriteObject.speed = math.sqrt(newXSpeed**2+newYSpeed**2)
        # print("SPEED CHANGE", spriteObject.speed)

        

        # #Sign = Opp/Hyp Cos = Adj/Hyp Tang=Opp/Adj
        # #x = adj = sin(angle)*speed
        # #y = opp = cos(angle)*speed
        
        # aclX = math.sin(math.radians(changeAngel))*changeAccel
        # aclY = math.cos(math.radians(changeAngel))*changeAccel

        # spdX = math.sin(math.radians(changeAngel))*changeSpeed # get speed if there is angle change
        # spdY = math.cos(math.radians(changeAngel))*changeSpeed

        # # print("SPRITE-X",spriteObject.speedX,"SPRIT-Y",spriteObject.speedY)
        # spriteObject.speedX = spdX
        # spriteObject.speedY = spdY

        # spriteObject.speedX += aclX
        # spriteObject.speedY += aclY
        
        
        # print("spdX",spdX,"spdY",spdY, "SPRITE-X",spriteObject.speedX,"SPRIT-Y",spriteObject.speedY)
        # # spriteObject.speed = 0 #we have speedX and speedY now. SO we will not need speed to change unless it is set.
        # # spriteObject.acceleration = 0 #set to zero as movement is given accelearation, this can change later



        
        # return spriteObject.move(int(spriteObject.speedX),int(spriteObject.speedY))

        

        

    

    def __updateCurrMove__(self): 
        '''updates currMove, as well as currBehavior and currSpeed'''
        if len(self.moveCounts)==0 and self.currMove==0:
            return True # this means there are no more moves to be made, so exitscreen will be checked or movement reset
        if self.currMove == 0:
            self.currMove = self.moveCounts.pop(0)
            if len(self.behaviors)>0:
                self.currBehavior = self.behaviors.pop(0)
            if len(self.speeds) >0:
                self.currSpeed = self.speeds.pop(0)
            if len(self.angles) > 0:
                self.currAngle = self.angles.pop(0)
            if len(self.vectors) > 0:
                self.currVector = self.vectors.pop(0)
                
        else: self.currMove -=1 #decrments 1 frame from move count
        return False
        
    def update(self,spriteObject):
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


