'''
File: weapon.py
01/29/19
'''


'''
MASTER WEAPONS DICTIONARY

Tuple Index:         |       0       |       1          |       2          |       3          |
Description:         | BULLET DAMAGE | BULLET FIRE RATE | IMAGE PATH       | BULLET FUNCTION  |
Units:               | 0-100 hp      | bullets per sec  | pathlib          | n/a              |
                     |               |                  |                  |
-----------------------------------------------------------------------------------------------
    WEAPON NAME      | BULLET DAMAGE | BULLET FIRE RATE | IMAGE PATH       | BULLET FUNCTION  |
                     |               |                  |                  |
   spitfire          |       10      |       4          |       n/a        |       n/a        |
   blue_lazer        |       10      |       4          |       n/a        |       n/a        |

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

def blue_lazer():
    print('blue lazer here')

master_weapons_dict = {
    'spitfire': (10, 4, weapon_images_path.joinpath('spitfire.png'), spitfire),
    'blue_lazer': (10, 4, weapon_images_path.joinpath('blue_lazer.gif'), blue_lazer)
}


class Weapon(object):

    def __init__(self, weaponName):

        if weaponName not in master_weapons_dict:
            raise Exception('the weapon must be in the master weapons dictionary.')
        self.name = weaponName
        self.weapon_damage = master_weapons_dict.get(weaponName)[0]
        self.rof = master_weapons_dict.get(weaponName)[1] # rof is the rate of fire in bullets per second
        self.weapon_image = master_weapons_dict.get(weaponName)[2]
        self.weapon_func = master_weapons_dict.get(weaponName)[3]

        #self.damage = master_weapons_dict.get(weaponName)[2]
        #print(damage)
        #print(master_weapons_dict.get('spitfire')[0])
        #print(self.weapon_image)
        #os.startfile(self.weapon_image)



if __name__=="__main__":
    def test():

        testWeapon = Weapon('spitfire')
        testWeapon2 = Weapon('blue_lazer')
        #os.startfile(testWeapon2.weapon_image)
        testWeapon.weapon_func()
    test()


