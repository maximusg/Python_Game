import pygame
from library import *
from pathlib import Path

cwd = Path.cwd()
bomb_explosion_images_path = cwd.joinpath('resources', 'weapon_images', 'bomb_explosion')
bomb_sounds = cwd.joinpath('resources', 'sound_effects', 'bomb_sounds')
#Constants
TOTAL_ANIM_FRAMES = 9

class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, startx, starty):
        super().__init__()
        anim0 = bomb_explosion_images_path.joinpath('bomb_explosion0.png')
        self.image, self.rect = load_image(str(anim0))
        self.rect = pygame.Rect(startx,starty,30,30)
        #self.radius = 25
        self.sound = load_sound(str(bomb_sounds.joinpath('Mboom.wav ')))
        self.frame_counter = 45
        self.frame = 1
        self.visible = 1
        self.bomb_growth = 1.1


    def update(self):
        if self.frame_counter == 0:
            self.visible = 0
        self.frame_counter -= 1
        if self.frame_counter % 5 == 0 and self.frame < TOTAL_ANIM_FRAMES:
            self.frame += 1
            old_x, old_y = self.rect.x, self.rect.y
            #self.image, self.rect = load_image('resources/weapon_images/bomb_explosion/bomb_explosion'+str(self.frame)+'.png')
            self.image, self.rect = load_image(str(bomb_explosion_images_path.joinpath('bomb_explosion')) + str(self.frame)+'.png')
            self.rect.x, self.rect.y = old_x, old_y
            self.size = self.image.get_size()
            # create a 2x bigger image than self.image
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*self.bomb_growth), int(self.size[1]*self.bomb_growth)))
            self.image = self.bigger_img
            self.bomb_growth += 0.2
        self.move(1,0)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        # draw bigger image to screen at x=100 y=100 position


    def move(self, diffx, diffy):
        self.rect = self.rect.move(diffx, diffy)

    def play_sound(self):
        self.sound.play()