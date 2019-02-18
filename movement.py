'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''
import copy

class Move(object):
    def __init__(self, behaviorArray=["down"], moveCountArray=[800], speedArray=[10], angelArray=[0], exitscreen=True):

        self.behaveDic = {
            "down": self.__down__, 
            "up":self.__up__, 
            "left":self.__left__, 
            "right":self.__right__, 
            "stop": self.__stop__,
            "northWest": self.__northWest__,
            "northEast": self.__northEast__,
            "soutWest": self.__southWest__,
            "southEast": self.__southEast__
            }

        self.save=[]
        if exitscreen==False:
            self.save.append(copy.deepcopy(behaviorArray))
            self.save.append(copy.deepcopy(moveCountArray))
            self.save.append(copy.deepcopy(speedArray)) #save to reinitialize arrays to loop movements

        self.behaviors = behaviorArray #list of methods to run from the behaveDic
        self.currBehavior = None
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.currMove = 0 
        self.speeds = speedArray #used to change speeds between behaviors, if no more speeds left, defaults to last speed given
        self.currSpeed = 0 
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
    
    def __northEast__(self,spriteObject):
        return spriteObject.move(self.currSpeed,-self.currSpeed)

    def __southEast__(self,spriteObject):
        return spriteObject.move(self.currSpeed,self.currSpeed)

    def __southWest__(self,spriteObject):
        return spriteObject.move(-self.currSpeed,self.currSpeed)

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
        else: self.currMove -=1 #decrments 1 frame from move count
        return False
        
    def update(self,spriteObject):
        
        if self.__updateCurrMove__(): # will initialize currSpeed, currMove, and currBehavior, and return True if no more moves left
            if not self.exitsceen: #will update reset the bahavior
                self.behaviors = copy.deepcopy(self.save[0]) 
                self.moveCounts = copy.deepcopy(self.save[1])
                self.speeds = copy.deepcopy(self.save[2]) 
                self.__updateCurrMove__()
            else: #will begin off screen behavior
                self.behaviors = ["down"] 
                self.moveCounts = [800]
                self.speeds = [10]
                self.__updateCurrMove__()
        
        spriteObject.move(0,1) #keeps ships constantly moving down
        updatedObject = self.behaveDic[self.currBehavior](spriteObject)
        
        return updatedObject

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


