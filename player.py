import entity2
import pygame
import bullet
import weapon



class player(entity2.entity2):
    def __init__(self, weapon, imgFile,scheme):
        super().__init__()
        self.weapon = weapon.Weapon(weapon)
        self.control_scheme = scheme ##placeholder
        self.point_total = 0
        self.image, self.rect = self.load_image(imgFile, -1)
        self.area = self.screen.get_rect()
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
        return bullet.bullet(origin_x, origin_y, 5, self.weapon.weapon_image)
    
    def control(self, bullet_count, FRAMERATE):
        keys = pygame.key.get_pressed()
        addBullet=False
        if self.control_scheme=="arrows":
            if keys[pygame.K_UP]:
                self.move(0,-self.speed)
            if keys[pygame.K_DOWN]:
                self.move(0,self.speed)
            if keys[pygame.K_LEFT]:
                self.move(-self.speed, 0)
            if keys[pygame.K_RIGHT]:
                self.move(self.speed, 0)
            if keys[pygame.K_SPACE]:
                if self.bullet_count % (int(FRAMERATE/self.weapon.rof)) == 0:
                    addBullet=True
                    bullet_count+=1
            return addBullet