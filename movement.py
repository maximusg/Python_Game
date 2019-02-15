'''
filename: movement.py

Purpose: describes movement patterns that enemies and items can have

Ideas: go down, left, right, up, circle, spiral, slow start then speed up, up and down
'''


class Move(object):
    def __init__(self, rect_to_move, angle, speed, move_limit = 30):

        #self.rect.centerx, self.rect.top = origin_x, origin_y

        #location
        #self.origin_x = origin_x
        #self.origin_y = origin_y

        self.rect = rect_to_move

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


