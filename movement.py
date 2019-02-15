'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''


class Move(object):
    def __init__(self, behaviorArray=["down"], moveCountArray=[800], speedArray=[10], exitscreen=True):

        behaveDic = {"down": self.__dive__(), "up":self.__up__(), 
        "left":self.__left__(), "right":self.__right__(), "stop": self.__stop__()}
 
        self.beaviors = behaviorArray #list of things to run from the behaveDic
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.currMove = None 
        self.__updateCurrMove__()
        self.speeds = speedArray #used to change speeds between behaviors, if no more speeds left, defaults to last speed given
        self.speed = self.__latestSpeed__() #method that will update the current speed from self.speeds,
        self.exitsceen = exitscreen #if true, this behaivor will result in enemy moving down and off screen after executing movements to be deleted else enemy will stay put




    def __up__(self):
        pass
    def __down__(self):
        pass
    def __left__(self):
        pass
    def __right__(self):
        pass
    def __stop__(self):
        pass
    def __updateCurrMove__():
        pass
    def __latestSpeed__():
        pass
    def Move(self):
        pass
    

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


