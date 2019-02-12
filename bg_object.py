import entity2
import pygame.mask
from library import *

class bg_object(pygame.sprite.DirtySprite):
	def __init__(self, origin_x, origin_y, speed, path_to_img, angle = 0):
		super().__init__()
		self.speed = speed
		self.image, self.rect = load_image(path_to_img, colorkey=(0,0,0))
		self.rect.centerx, self.rect.top = origin_x, origin_y
		self.dirty = 2
		self.angle = angle
		self.mask = pygame.mask.from_surface(self.image)
		self.layer = 2

	def move(self):
		self.rect = self.rect.move(self.angle,self.speed)
		#self.dirty = 1

	def update(self):
		if self.rect.top < SCREEN_HEIGHT and self.rect.left < SCREEN_WIDTH-COLUMN_WIDTH and self.rect.right > COLUMN_WIDTH:
			self.move()
		else:
			self.visible = 0

