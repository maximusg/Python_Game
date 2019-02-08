import entity2
from library import *



class enemy(entity2.entity2):
	def __init__(self, weapon, imgFile):
		super().__init__()
		self.weapon = weapon
		self.point_value = 500
		self.image, self.rect = load_image(imgFile)
		self.rect.centerx, self.rect.top = 300, 50
		self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)
		self.speed = 4
	
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
		self.move(self.speed, 0)