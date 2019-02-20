import entity2
import bullet
import movement

from library import *
from levelLibrary import *

import itemDropTables
import item_pickup
import random

class enemy(entity2.entity2):
	def __init__(self, origin=ENEMY_SECTORS("s4"), imgFile="enemy.png", speed=1, behavior="diver", weapon="spitfire", health=1, itemDropTable = itemDropTables.common):
		super().__init__()
		self.weapon = weapon
		self.point_value = 500
		self.imgFile = 'enemy'+str(random.randint(1,3))+'.png'
		self.image, self.rect = load_image(self.imgFile)
		#self.rect.centerx, self.rect.top = 300, 50
		self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
		self.speed = speed #this will be a scaler for movement type
		self.health = health
		self.rect.x = origin[0]
		self.rect.y = origin[1]
		

		self.behaveDic = {
			"diver":self.__diver__, 
			"camper":self.__camper__, 
			"sleeper":self.__sleeper__,
			"crazy":self.__crazy__,
			"crazyReverse": self.__crazyReverse__
			}
		
		self.movement = self.behaveDic[behavior]()

		#item drops
		self.itemDropTable = itemDropTable

	def __diver__(self):
		return movement.Move(speedArray=[1*self.speed]) #default behavior for object, could increase/decrease speed
	
	def __camper__(self):#stays on the screen camping, will progress down the screen slowly doing squares
		behaviorArray = ["down","stop","left","stop","up","stop","right"]
		moveCountArray = [80,	20,	40,		20,  50,	20,	40]
		speedArray = [	  1*self.speed,	1*self.speed]
		return movement.Move(behaviorArray,moveCountArray,speedArray,exitscreen=False)

	def __crazy__(self):
		behaviorArray = ["down","left","right","down","up","down"]
		angleArray =    [0,		-90,	90,		0,		180, 0]
		moveCountArray = [20,	20,	20,	20,   20,	20]
	
		speedArray = [	  1*self.speed,	2*self.speed, 1*self.speed,	3*self.speed,1*self.speed,	2*self.speed]
		return movement.Move(behaviorArray,moveCountArray,speedArray,angleArray,exitscreen=False)

	def __crazyReverse__(self):
		behaviorArray = ["down","stop","up","down","right","left","down"]
		moveCountArray = [20,	20,	20,	20,   20,	20,	    20]
		speedArray = [	  1*self.speed,	2*self.speed, 1*self.speed,	3*self.speed,1*self.speed,	2*self.speed]
		return movement.Move(behaviorArray,moveCountArray,speedArray,exitscreen=False)

	def __sleeper__(self):# moves down and stops for a LLLONG time =, the wiggles left and right FAST, the stops again, the dives down
		behaviorArray = ["down","stop","left","right"]
		moveCountArray = [80,	100,	40,		40]
		speedArray = [	  1*self.speed,	1*self.speed]
		return movement.Move(behaviorArray,moveCountArray,speedArray)
	
	def move(self, x, y):
		if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
			self.rect.left = self.area.left
			self.speed = -self.speed
		elif self.rect.right > self.area.right:
			self.rect.right = self.area.right
			self.speed = -self.speed
		else:
			self.rect = self.rect.move((x, y))
		self.dirty = 1

	def update(self):
		# self=self.movement.update(self)
		bullet_to_add = []
		self.movement.update(self)
		if not (COLUMN_WIDTH <= self.rect.right and self.rect.left <= SCREEN_WIDTH-COLUMN_WIDTH):
			self.visible = 0
		if not (0 <= self.rect.top <= SCREEN_HEIGHT):
			self.visible = 0
		if self.visible:
			if random.random() <= 0.01:
				bullet_to_add.append(bullet.bullet(self.rect.centerx, self.rect.centery, 20, 'resources/weapon_images/spitfire.png', behavior='down'))
		return bullet_to_add

	def getDrop(self):
		#build the working drop table
		items = []
		probability = []
		total_probability = 0
		rand_num = random.uniform(0,1)
		droppedItem = None
		for item in self.itemDropTable:
			items.append(item[0])
			probability.append(total_probability + float(item[1]))
			total_probability += float(item[1])
			#if total_probability > 1:
			#	raise RunTimeError('probabilities cannot add up to more than 1')

		intervals = []
		curr_prob = 0

		for i in range(len(probability)):
			intervals.append((curr_prob, probability[i]))
			curr_prob += probability[i]
			if rand_num >= intervals[i][0] and rand_num <= intervals[i][1]:
				droppedItem = items[i]
		#add more logic on what to do with the dropped item later
		#print(droppedItem) #debugging
		if droppedItem is None:
			return None
		else:
			return item_pickup.item(self.rect.centerx, self.rect.centery, name= droppedItem)