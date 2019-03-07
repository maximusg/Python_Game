import pygame
from library import *

class ExplosionSprite(pygame.sprite.Sprite):
    def __init__(self, startx, starty, direction='down'):
        super().__init__()
        self.image, self.rect = ASSET_MANAGER.getAsset('resources/misc_sprites/explosion1.png')
        self.rect = pygame.Rect(startx,starty,30,30)
        self.sound = load_sound('explosion.ogg')
        self.direction = direction
        self.frame_counter = 45
        self.frame = 1
        self.visible = 1

    def update(self):
        if self.frame_counter == 0:
            self.visible = 0
        self.frame_counter -= 1
        if self.frame_counter % 5 == 0 and self.frame < 7:
            self.frame += 1
            old_x, old_y = self.rect.x, self.rect.y
            self.image, self.rect = ASSET_MANAGER.getAsset('resources/misc_sprites/explosion'+str(self.frame)+'.png')
            self.rect.x, self.rect.y = old_x, old_y
        if self.direction == 'down':
            self.move(0,5)
        elif self.direction == 'up':
            self.move(0,-5)

    def move(self, diffx, diffy):
        self.rect = self.rect.move(diffx, diffy)

    def play_sound(self):
        self.sound.play()