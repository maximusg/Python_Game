import pygame

class control_scheme():
	def __init__(self, playerShip, bullet_count, FRAMERATE, scheme):

		self.keys = pygame.key.get_pressed()
		self.addBullet=False
		self.playerShip=playerShip
		self.bullet_count=bullet_count
	def arrows(self):
		if self.keys[pygame.K_UP]:
			self.playerShip.move(0,-self.playerShip.speed)
		if self.keys[pygame.K_DOWN]:
			self.playerShip.move(0,self.playerShip.speed)
		if self.keys[pygame.K_LEFT]:
			self.playerShip.move(-self.playerShip.speed, 0)
		if self.keys[pygame.K_RIGHT]:
			self.playerShip.move(self.playerShip.speed, 0)
		if self.keys[pygame.K_SPACE]:
			if self.bullet_count % (int(FRAMERATE/self.playerShip.weapon.rof)) == 0:
				self.addBullet=True
				self.bullet_count+=1
		return (self.playerShip,self.addBullet,self.bullet_count)