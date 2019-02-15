'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''


class Move(object):
    def __init__(self, rect_to_move, behaviorArray, moveCountArray, speedArray=10, exitscreen=True):

        behaveDic = {"dive": self.__dive__(), "up":self.__up__(), 
        "left":self.__left__(), "right":self.__right__()}
 
        self.beaviors = behaviorArray #list of things to run from the behaveDic
        self.moveCounts = moveCountArray# array frame amounts to do move count
        self.speeds = speedArray #used to change speeds between behaviors, if no more speeds left, defaults to last speed given
        self.speed = self.latestSpeed() #method that will update the current speed from self.speeds,
        self.exitsceen = exitscreen #if true, this behaivor will result in enemy off screen and gone
        
        #execute default behaviors

        
        #self.rect.centerx, self.rect.top origin_x, origin_y

        #location
        #self.origin_x = origin_x
        #self.origin_y = origin_y

        self.rect = rect_to_move
        self.rect

        #angle and speed
        self.angle = angle
        self.speed = speed

        #move limit is how much is moved before changing behavior, reversed and move_counter can be used to track this
        self.move_limit = move_limit
        self.reversed = False
        self.move_counter = 0

        print(id(self.rect), self.angle, self.speed, self.move_limit)

    def upAndDown(self):
        if self.reversed == False:
                self.rect = self.rect.move(self.angle,-self.speed)
                self.move_counter += 1

                if self.move_counter == self.move_limit:
                    self.reversed = True

        elif self.reversed == True:

            self.rect = self.rect.move(self.angle, self.speed)
            self.move_counter -= 1

            if self.move_counter == 0:
                self.reversed = False


