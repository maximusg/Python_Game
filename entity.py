#Entity.py
#
# Implements ships as entities. 
# by: Christopher Norine
# Last updated: 17 January 2019
#

##import section
import pygame

##class defs
class Point(object):
    def __init__(self, xIn, yIn):
        self.x = xIn
        self.y = yIn

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, xIn):
        if not isinstance(xIn, int) and not isinstance(xIn, float):
            raise RuntimeError(xIn + ' is not a valid value for Point.xIn.')  
        self.__x = xIn  
    
    @y.setter
    def y(self, yIn):
        if not isinstance(yIn, int) and not isinstance(yIn, float):
            raise RuntimeError(yIn + ' is not a valid value for Point.yIn.')  
        self.__y = yIn  

    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'

class entity(object):
    def __init__(self):
        self.location = None
        self.health = 100
        self.sprite = None
        self.weapon = Weapon()

        @property
        def location(self):
            return self.__location

        @location.setter
        def location(self, new_point):
            if not isinstance(new_point, Point):
                raise RuntimeError(new_point + ' is not a valid Point for update.')
            self.__location = new_point

        @property
        def health(self):
            return self.__health
        
        @health.setter
        def health(self, value):
            if not isinstance(value, int):
                raise RuntimeError(value + ' is not a valid int for health.')
            self.__health = value

        @property
        def sprite(self):
            return self.__sprite
        
        @sprite.setter
        def sprite(self, new_sprite):
            ###figure out error checking for this
            self.__sprite = new_sprite

        @property
        def weapon(self):
            return self.__weapon

        @weapon.setter
        def weapon(self, new_weapon):
            if not isinstance(new_weapon, Weapon):
                raise RuntimeError(new_weapon + ' is not a valid weapon class.')


class player_ship(entity):
    def __init__(self):
        pass

class enemy(entity):
    def __init__(self):
        pass


    

