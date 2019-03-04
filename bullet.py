import entity2
import pygame.mask
import movement
from library import *

#CONSTANTS for vector methods, need to find a good home for these
DEFAULT =["x","x","x"] #whatever the settings for sprite are, continue
UP = ["x","x",180]
DOWN = ["x","x",0]
LEFT = ["x","x",-90]
RIGHT = ["x","x",90]

class bullet(entity2.entity2):
	def __init__(self, origin_x, origin_y, speed, path_to_img, acceleration=0, angle = 0, behavior = 'up'):
		location =(origin_x, origin_y)
		super().__init__(origin=location, imageFile=path_to_img, speed=speed, acceleration=acceleration, angle=angle )

		self.dirty = 1
		self.mask = pygame.mask.from_surface(self.image)
		

		#in order to reuse in other methods.
		self.NE = ["x", self.speed*0.5 ,(180+30)]
		self.NNE = ["x", self.speed*0.5 ,(180+15)]
		self.NW = ["x", self.speed*0.5 ,(180-30)]
		self.NNW = ["x", self.speed*0.5 ,(180-15)]


		self.behaveDic = {
			"up":self.__up__,
			"northWest":self.__northWest__,
			"northEast":self.__northEast__,
			"northNorthEast":self.__northNorthEast__,
			"northNorthWest":self.__northNorthWest__,
			"missle":self.__missleLeft__,
			"down":self.__down__,
			"vector":self.__vector__
			}

		self.movement = self.behaveDic[behavior]()


	def move(self, x, y):

		self.rect = self.rect.move((x, y))
		self.dirty = 1

	def update(self):
		if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.right > SCREEN_WIDTH-COLUMN_WIDTH or self.rect.left < COLUMN_WIDTH: #checks if the rect is out of bounds, and if so, it is no longer visible, meaning it should be deleted by GUI
			self.visible = 0
			self.dirty = 1

		self.movement.update(self)

	
	def __up__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[UP] ) 

	def __northEast__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[self.NE]) 

	def __northNorthEast__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[self.NNE])  

	def __northWest__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[self.NW]) 

	def __northNorthWest__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[self.NNW]) 

	def __missleLeft__(self):

		accelerateUp = [2,"x",180] #sets acceleration to 2
		moveCountArray = [5,1,800]
		
		return movement.Move(moveCountArray=moveCountArray, vectorAray=[self.NW,accelerateUp,DEFAULT]) #uses "DEFAULT"to keep the missle moving

	def __down__(self):
		return movement.Move(moveCountArray=[800], vectorAray=[DOWN] ) 

	def __vector__(self):
		vector = ["x",self.speed,self.angle]
		return movement.Move(moveCountArray=[1000],vectorAray=[vector])