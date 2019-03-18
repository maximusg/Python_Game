import copy
import math

import pygame

from library import *


class Move(object):#REMOVE behaviorArray, SpeedArray, and AngelArray, Replace exitScreen with  "times to repeat"
    '''
    Purpose: describes movement patterns that enemies and items can have

    Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
    '''
    def __init__(self, moveCountArray=[800], vectorAray=[["x",3,0]], repeat=3):
        '''moveCountArray: an array of ints will move an object each frame number of times, for each int in array
            vactorAray: is a list of lists. Each list in the list contains vector information [[acceleration,speed,angle]] 
            example[[0,1,75]] current Move count will execute the vector the number of moves in the moveCount int, and 
            shift both vectorArray and moveCountArray when current moveCount runs to zero. If size of moveCountArray is
            larger than vectorArray, the last vector in vector array will continue to be exectued until all ints in
            moveCount array have shifted out and counted down to zero.
            repeat: reapeat is an int which loops both moveCountArray and VectorAray. If repeat =-1, then the object
            will default to a moveCountArray=[1,10000] and vector=[[2,0,0]] where the objects acceleration will get set
            to 2 speed to 0, angle to 0 (down) and it will speed up off the screen using acceleration to add 2 pixels 
            of speed in the downward direction each frame'''
        

        self.save=[]#save to reinitialize arrays to loop movements
        self.save.append(copy.deepcopy(moveCountArray))
        self.save.append(copy.deepcopy(vectorAray))
        # print("movecountArray",moveCountArray)
        self.moveCounts = moveCountArray# array frame amounts to do move count
        # print("self.movCounts", self.moveCounts)
        self.currMove = 0 
        self.repeat = repeat
       
       #NEW STUFF HERE
        self.currVector = [0,0,0]
        # [entityAcceleration, entitySpeed, entityAngle]
        self.vectors = vectorAray # contains a list frames to go through for each speed accerlation and angle change
    
    
    ##########LISTS###############
    @property
    def save(self):
        return self.__save
    
    @save.setter
    def save(self, value):
        if not isinstance(value, list):
            raise RuntimeError(str(value) + ' is not a valid list for save.')
        self.__save = value
    
    @property
    def moveCounts(self):
        return self.__moveCounts
    
    @moveCounts.setter
    def moveCounts(self, value):
      
        if not isinstance(value, list):
            raise RuntimeError(str(value) + ' is not a valid list for moveCounts.')
        if not all(isinstance(i,int) for i in value):
            raise RuntimeError(str(value) + ' is not a valid list of ints for moveCounts.')
      
        self.__moveCounts = value



    @property
    def vectors(self):
        return self.__vectors
    
    @vectors.setter
    def vectors(self, value):
        if not isinstance(value, list):
            raise RuntimeError(str(value) + ' is not a valid list for vectors.')
        if not all(isinstance(i,list) for i in value):
            raise RuntimeError(str(value) + ' is not a valid list of lists in vectors.')
        if not all(isinstance(j,float) or isinstance(j,int) or j=="x" for i in value for j in i): #checks all types allowed for vector input
            
            raise RuntimeError(str(value) + ' is not a valid number or "x" in list of lists in vectors.')
        self.__vectors = value
    
    ##########Curr Value Checks##############
    @property
    def currMove(self):
        return self.__currMove
    
    @currMove.setter
    def currMove(self, value):
        if not isinstance(value, int):
            raise RuntimeError(str(value) + ' is not a valid int for currMove.')
        self.__currMove = value

    @property
    def currVector(self):
        return self.__currVector
    
    @currVector.setter
    def currVector(self, value):
        if not isinstance(value, list):
            raise RuntimeError(str(value) + ' is not a valid list for currVector.')
        self.__currVector = value
    
    @property
    def repeat(self):
        return self.__repeat
    
    @repeat.setter
    def repeat(self, value):
        if not (isinstance(value, int)):
            raise RuntimeError(str(value) + ' is not a valid int for repeat.')
       
        
        self.__repeat = value
        

    def __vector__ (self,spriteObject):
        '''does all the vetor math after seting acceleration, speed, and angle of an Entity object and then updating
        the entity to tack on the acceleration to speed.'''
        #print(spriteObject.speedY)
        changeAccel = self.currVector[0]
        changeSpeed = self.currVector[1]
        changeAngel = self.currVector[2]
        
        #speed v= Dv + a[frame]
        
        #check for x, will update sprite values if not x.
        if changeAccel != "x":
            spriteObject.acceleration = changeAccel
        if changeAngel != "x": #when angle changes, spriteObject.speed, .speedX and .speedY all update w/ new values
            spriteObject.angle = changeAngel
        if changeSpeed != "x":
            spriteObject.speed= changeSpeed #adjusts spriteObject.speed, .speedX, and .speedY appropriately on object
       
        spriteObject.updateSpeed() #accelerates object by adding spriteObject.acceleration to its .speedX and .speedY
        
        spriteObject.move(int(spriteObject.speedX),int(spriteObject.speedY)) #updates spriteObject.x and .y approprately

        return spriteObject

    

    def __updateCurrMove__(self): 
        '''updates currrent move, along the vector'''
        if len(self.moveCounts)==0 and self.currMove==0:
            return True # this means there are no more moves to be made, so exitscreen will be checked or movement reset
        if self.currMove <= 0:
            # print ("movecounts",self.moveCounts)
            self.currMove = self.moveCounts.pop(0)
            if len(self.vectors) > 0:
                self.currVector = self.vectors.pop(0)
            
        
        else: self.currMove -=1 #decrments 1 frame from move count
        return False
        
    def update(self,spriteObject):
        ''' updates sprites coordinates based off contructed move sets returns and updated object which can be put in
            a GUI'''

        if self.__updateCurrMove__(): # will initialize currSpeed, currMove, and currBehavior, and return True if no more moves left
            if self.repeat>0: #will update reset the bahavior
                self.moveCounts = copy.deepcopy(self.save[0])
                self.vectors = copy.deepcopy(self.save[1])
               
                self.__updateCurrMove__()
            else: #will begin off screen behavior
                self.moveCounts = [1,800]
                self.vectors=[[2,0,0], ["x","x","x"]]#sets acceleration to 2 and exits screen
                self.__updateCurrMove__()
            
            self.repeat -=1
        
        updatedObject = self.__vector__(spriteObject)
        
        return updatedObject

 



