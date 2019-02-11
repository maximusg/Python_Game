import entity2
import pygame.mask
from library import *

class bullet(entity2.entity2):
	def __init__(self, origin_x, origin_y, speed, path_to_img, angle = 0):
		super().__init__()
		self.speed = speed
		self.image, self.rect = load_image(path_to_img)
		self.image = self.image.convert()
		self.rect.centerx, self.rect.top = origin_x, origin_y
		self.off_screen = False
		self.dirty = 1
		self.mask = pygame.mask.from_surface(self.image)
		self.angle = angle

	def move(self):
		self.rect = self.rect.move(self.angle,-self.speed)
		self.dirty = 1

	def update(self):
		if self.rect.bottom > 0 and self.rect.right < SCREEN_WIDTH-COLUMN_WIDTH and self.rect.left > COLUMN_WIDTH:
			self.move()
		else:
			self.visible = 0
			self.dirty = 1
