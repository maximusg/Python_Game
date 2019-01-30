import entity2
import pygame.mask

class bullet(entity2.entity2):
	def __init__(self, origin_x, origin_y, speed, path_to_img):
		super().__init__()
		self.speed = speed
		self.image, self.rect = self.load_image(path_to_img)
		self.image = self.image.convert()
		self.rect.centerx, self.rect.top = origin_x, origin_y
		self.off_screen = False
		self.dirty = 1
		self.mask = pygame.mask.from_surface(self.image)

	def move(self):
		self.rect = self.rect.move(0,-self.speed)
		self.dirty = 1

	def update(self):
		if self.rect.bottom > 0:
			self.move()
		else:
			self.visible = 0
			self.dirty = 1