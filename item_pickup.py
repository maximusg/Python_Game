import entity2
import weapon
from pathlib import Path
from library import *

cwd = Path.cwd()
item_images_path = cwd.joinpath('resources', 'item_images')

master_items_dict = {
    'powerup':('powerup.gif', None),
    'coin':('coin.png', None),
    'spitfire_powerup':('spitfire_powerup.png', 'spitfire')
}


class item(entity2.entity2):
    def __init__(self, origin_x, origin_y, speed = 1, path_to_img = 'powerup.gif', name = None):
        super().__init__()

        self.weapon_name = None
        if name is not None:
            if name in master_items_dict:
                path_to_img = master_items_dict.get(name)[0]
                weapon_name = master_items_dict.get(name)[1]
                self.is_weapon = weapon.is_weapon(weapon_name)
                if self.is_weapon:
                    self.weapon_name = self.is_weapon

        self.image, self.rect = load_image(item_images_path.joinpath(path_to_img))
        self.rect.centerx, self.rect.top = origin_x, origin_y
        self.dirty = 1


        self.name = name


        #for item movement
        self.speed = speed


    def move(self, x, y):
        self.rect = self.rect.move((x, y))
        self.dirty = 1

    def update(self):
        if self.rect.bottom < 0 or self.rect.right > SCREEN_WIDTH-COLUMN_WIDTH or self.rect.left < COLUMN_WIDTH: #checks if the rect is out of bounds, and if so, it is no longer visible, meaning it should be deleted by GUI
            self.visible = 0
            self.dirty = 1

        self.move(0,self.speed)#moves straight down at a given speed

