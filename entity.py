#Entity.py
#
# Implements ships as entities. 
# by: Christopher Norine
# Last updated: 17 January 2019
#

##import section
import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
import weapon

main_dir = os.path.split(os.path.abspath(__file__))[0]

# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(main_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class entity(pygame.sprite.DirtySprite):
	def __init__(self):
		super().__init__()
		self.health = 1

		@property
		def health(self):
			return self.__health
		
		@health.setter
		def health(self, value):
			if not isinstance(value, int):
				raise RuntimeError(value + ' is not a valid int for health.')
			self.__health = value

class player_ship(entity):
	def __init__(self):
		super().__init__()
		self.weapon = weapon.Weapon('spitfire')
		self.control_scheme = 'wasd' ##placeholder
		self.point_total = 0
		self.image, self.rect = load_image('SweetShip.png', -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 500,600
		self.speed = 10

	def move(self, new_x, new_y):
		if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
			self.rect.left = self.area.left
		elif self.rect.right > self.area.right:
			self.rect.right = self.area.right
		elif self.rect.top < self.area.top:
			self.rect.top = self.area.top
		elif self.rect.bottom > self.area.bottom:
			self.rect.bottom = self.area.bottom
		else:
			self.rect = self.rect.move((new_x, new_y))
		self.dirty = 1

	def fire(self):
		origin_x = (self.rect.left + self.rect.right) / 2
		origin_y = self.rect.top
		return bullet(origin_x, origin_y, 5, self.weapon.weapon_image)
	
class enemy(entity):
	def __init__(self):
		super().__init__()
		self.weapon = 'enemy_spitfire'
		self.point_value = 500
		self.image, self.rect = load_image('enemy.png')
		self.rect.centerx, self.rect.top = 300, 50
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
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


class bullet(pygame.sprite.DirtySprite):
	def __init__(self, origin_x, origin_y, speed, path_to_img):
		super().__init__()
		self.speed = speed
		self.image, self.rect = load_image(path_to_img)
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

	

