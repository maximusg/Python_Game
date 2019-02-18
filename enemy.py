import entity2
import movement
from library import *



class enemy(entity2.entity2):
	def __init__(self, origin=ENEMY_SECTORS["s4"], imgFile="enemy.png", speed=1, behavior="diver", weapon="spitfire", health=1):
		super().__init__()
		self.weapon = weapon
		self.point_value = 500
		self.image, self.rect = load_image(imgFile)
		#self.rect.centerx, self.rect.top = 300, 50
		self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
		self.speed = speed #this will be a scaler for movement type
		self.health = health
		self.rect.x = origin[0]
		self.rect.y = origin[1]

		self.behaveDic = {
			"diver":self.__diver__, 
			"camper":self.__camper__, 
			"sleeper":self.__sleeper__
			}
		
		self.movement = self.behaveDic[behavior]()

	def __diver__(self):
		return movement.Move(speedArray=[1*self.speed]) #default behavior for object, could increase/decrease speed
	
	def __camper__(self):#stays on the screen camping, will progress down the screen slowly doing squares
		behaviorArray = ["down","stop","left","stop","up","stop","right"]
		moveCountArray = [80,	100,	40,		100,  50,	100,	40]
		speedArray = [	  1*self.speed,	1*self.speed]
		return movement.Move(behaviorArray,moveCountArray,speedArray,False)
	

	def __sleeper__(self):# moves down and stops for a LLLONG time =, the wiggles left and right FAST, the stops again, the dives down
		behaviorArray = ["down","stop","left","right"]
		moveCountArray = [80,	600,	40,		40]
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
		self.movement.update(self)
		if not (COLUMN_WIDTH <= self.rect.right and self.rect.left <= SCREEN_WIDTH-COLUMN_WIDTH):
			self.visible = 0
		if not (0 <= self.rect.top <= SCREEN_HEIGHT):
			self.visible = 0