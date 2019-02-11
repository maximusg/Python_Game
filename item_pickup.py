import entity2
import pygame.mask
import weapon
from library import *

class item(entity2.entity2):
    def __init__(self, origin_x, origin_y, speed, path_to_img, angle = 0, name = None):
        super().__init__()
        self.speed = speed
        print('path to img', path_to_img)
        self.image, self.rect = load_image(path_to_img)
        self.image = self.image.convert()
        self.rect.centerx, self.rect.top = origin_x, origin_y
        self.off_screen = False
        self.dirty = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle
        self.move_counter = 0
        self.move_limit = 30
        self.reversed = False
        self.name = name


        #weapon specific attributes
        self.is_weapon = False #can quickly check if it is a weapon

        if name in weapon.master_weapons_dict.keys():
            #if the name of the item is in the master weapons dictionary then it is a Weapon
            self.is_weapon = True


    #I added self.move_counter, move_limit, and reversed to make the item move back and forth, kind of like the bad guy
    def move(self):
        if self.reversed == False:
            self.rect = self.rect.move(self.angle,-self.speed)
            self.move_counter += 1
            if self.move_counter == self.move_limit:
                self.reversed = True
        elif self.reversed == True:
            self.rect = self.rect.move(self.angle, self.speed)
            self.move_counter -= 1
            if self.move_counter == 0:
                self.reversed = False
        self.dirty = 1

    def update(self):
        if self.rect.bottom > 0 and self.rect.right < SCREEN_WIDTH-COLUMN_WIDTH and self.rect.left > COLUMN_WIDTH:
            self.move()
        else:
            self.visible = 0
            self.dirty = 1
            print('i died') #DEBUGGING, remove when done

