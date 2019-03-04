import entity2
import bullet
import movement

from library import *
from levelLibrary import *

import itemDropTables
import item_pickup
import random

class enemy(entity2.entity2):
	def __init__(self, origin=ENEMY_SECTORS("s4"), imgFile="enemy.png", speed=1, behavior="diver", weapon="spitfire", health=1, acceleration=0, itemDropTable = itemDropTables.common, angle=0):
		
		imgFile = 'enemy'+str(random.randint(1,3))+'.png'
		area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)

		super().__init__(origin=origin, imageFile=imgFile, area=area, speed=speed, acceleration=acceleration, angle=angle, health=health)
		self.weapon = weapon
		self.point_value = 500
		
		# self.image, self.rect = load_image(self.imgFile)
		#self.rect.centerx, self.rect.top = 300, 50
		
		# self.rect.x = origin[0]
		# self.rect.y = origin[1]
		self.speed=speed
		
		# print("ENEMY ", behavior, origin, acceleration)

		self.behaveDic = {
			"diver":self.__diver__, 
			"camper":self.__camper__, 
			"sleeper":self.__sleeper__,
			"crazy":self.__crazy__,
			"crazyReverse": self.__crazyReverse__,
			"mrVectors": self.__mrVectors__,
			"diveBomb": self.__diveBomb__,
			"diveStrafe": self.__diveStrafe__
			}
		
		
		self.movement = self.behaveDic[behavior]()

		#item drops
		self.itemDropTable = itemDropTable

	def __diver__(self):
		dive=["x",3,"x"]
		return movement.Move(moveCountArray=[100000],vectorAray=[dive])
	
	def __camper__(self):#stays on the screen camping, will progress down the screen slowly doing squares
		
		moveCountArray = [80,	20,	40,		20,  50,	20,	40]
		down =["x","x",0]#comes down at spawn speed
		stop = [0,0,0]
		left = [0,3,-90]
		right = ["x","x",90]
		up = ["x","x",180]

		moveCountArray = [20,	20,	20,	20,   20,	20,	    20]
		vectorArray = [down, stop, left, stop, up, stop, right]
		
		return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

	def __crazy__(self):
		
		down =["x","x",0]#comes down at spawn speed
		stop = [0,0,0]
		left = [0,3,-90]
		right = ["x","x",90]
		up = ["x","x",180]

		moveCountArray = [20,	20,	20,	20,   20,	20,	    20]
		vectorArray = [down, left, right, down, up, stop, down]
		
		return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

	def __crazyReverse__(self):
		down =["x","x",0]#comes down at spawn speed
		stop = [0,0,0]
		left = [0,3,-90]
		right = ["x","x",90]
		up = ["x","x",180]

		moveCountArray = [20,	20,	20,	20,   20,	20,	    20]
		vectorArray = [down, stop, up, down, right, left, down]
		
		return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

	def __sleeper__(self):# moves down and stops for a LLLONG time =, the wiggles left and right FAST, the stops again, the dives down
		behaviorArray = ["down","stop","left","right"]
		down =["x","x",0]#comes down at spawn speed
		stop = [0,0,0]
		left = [0,3,-90]
		right = ["x","x",90]
		moveCountArray = [80,	100,	40,		40]
		vectorArray = [down,stop,left,right]
		return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

	def __mrVectors__(self): #implements vector movements
		#vector = [acceleration, speed, angle] if there is an "x" 
		# you will use the entities default, which if not set is 0.

		#couple of examples
		down = [1,"x",0]#accelerate down 1 frame more each time
		up = [1,"x",180]
		northEast =[.4,"x", 46] #note you can use fractions for acceleration
		turn_right = [0,3,90] # speed must be combined wtih an angle or it wont change anything
		turn_left = [1,"x",180]
		stop =		[0,0,0]

		#fill the vector array to execute each moveCount
		vectorArray = [ down, up,turn_right, stop]
		#still uses frame count
		moveCountArray = [10,21, 10, 30]
		return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=10)
	
	##NEW##
	def __diveBomb__(self):
		dive=["x","x","x"]
		return movement.Move(moveCountArray=[100000],vectorAray=[dive])
	
	##NEW##
	def __diveStrafe__(self):
	
		diveLeft=["x","x",45]
		diveRight=["x","x",-45]

		return movement.Move(moveCountArray=[25,25],vectorAray=[diveLeft,diveRight],repeat=10)



	

	def update(self):
		# self=self.movement.update(self)
		bullet_to_add = []
		self.movement.update(self)
		
		if not (COLUMN_WIDTH <= self.rect.right and self.rect.left <= SCREEN_WIDTH-COLUMN_WIDTH):
			self.visible = 0
		if not (0 <= self.rect.centery <= SCREEN_HEIGHT):
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

	def take_damage(self, value):
		self.health -= value
		if self.health <= 0:
			self.visible = 0


