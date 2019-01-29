'''
File: weapon.py
01/28/19
'''


'''
MASTER WEAPONS DICTIONARY

Tuple Index:         |       0       |       1          |       2          |       3          |
Description:         | BULLET DAMAGE | BULLET FIRE RATE | IMAGE PATH       | BULLET FUNCTION  |
Units:               | 0-100         | bullets per sec  | pathlib          | n/a

'''

import os
from pathlib import Path


cwd = Path.cwd()
weapon_images_path = cwd.joinpath('resources', 'weapon_images')
#os.startfile(weapon_images_path)

#spitfire_path = cwd.joinpath('/resources/weapon_images')
#print(cwd)
#print(spitfire_path)
#print(spitfire_path)
#for x in spitfire_path.iterdir():
#    if x.is_file():
#        print(x)
#each weapon name will be mapped to its function, an image, and other properties
def spitfire():
    print('spitfire here')

master_weapons_dict = {
    'spitfire': (10, 4, weapon_images_path.joinpath('spitfire.png'), spitfire())

}


class Weapon(object):

    def __init__(self, weaponName):
        self.name = weaponName
        self.weapon_func = master_weapons_dict.get(weaponName)[0]
        self.weapon_image = master_weapons_dict.get(weaponName)[2]
        self.rof = master_weapons_dict.get(weaponName)[1]
        #self.damage = master_weapons_dict.get(weaponName)[2]
        #print(damage)
        #print(master_weapons_dict.get('spitfire')[0])
        #print(self.weapon_image)
        #os.startfile(self.weapon_image)


testWeapon = Weapon('spitfire')
#testWeapon.weapon_func()