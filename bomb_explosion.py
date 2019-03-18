import pygame
from library import *

#Constants
TOTAL_ANIM_FRAMES = 9

class BombExplosion(pygame.sprite.Sprite):
    '''Sprite class for the large bomb explosions!.'''

    def __init__(self, startx, starty):
        '''Initialize the sprite at location (startx,starty).'''

        super().__init__()
        anim0 = BOMB_EXPLOSION_PATH.joinpath('bomb_explosion0.png')
        self.image, self.rect = ASSET_MANAGER.getAsset(str(anim0))
        self.rect = pygame.Rect(startx-150,starty-150,300,300)
        self.sound = load_sound(str(BOMB_SOUND_PATH.joinpath('Mboom.wav')))
        self.frame_counter = 45
        self.frame = 1
        self.visible = 1
        self.bomb_growth = 1


    def update(self):
        '''Update sprite, moving it as necessary and changing the image based on time.'''
        if self.frame_counter == 0:
            self.visible = 0
        self.frame_counter -= 1
        if self.frame_counter % 5 == 0 and self.frame < TOTAL_ANIM_FRAMES:

            bomb_size = self.image.get_size()
            self.frame += 1
            old_x, old_y = self.rect.centerx, self.rect.centery
            self.image, self.rect = ASSET_MANAGER.getAsset(str(BOMB_EXPLOSION_PATH.joinpath('bomb_explosion')) + str(self.frame)+'.png')
            self.rect.centerx, self.rect.centery = old_x, old_y
            self.image = pygame.transform.scale(self.image, (int(bomb_size[0]*self.bomb_growth), int(bomb_size[1]*self.bomb_growth)))
            self.rect = self.image.get_rect(center=(old_x,old_y))
            self.bomb_growth += 0.066 #changing this value will change how much the explosion grows each frame. Anything above 0.75 is bad, explosion fills the whole screen



    def move(self, diffx, diffy):
        '''Move rect by (diffx, diffy).'''
        self.rect = self.rect.move(diffx, diffy)

    def play_sound(self):
        '''Play sound.'''
        self.sound.play()