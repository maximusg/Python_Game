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
import player
import bullet
import movement

cwd = Path.cwd()
weapon_images_path = cwd.joinpath('resources', 'weapon_images')

#each weapon name will be mapped to its function, an image, and other properties

def spitfire(origin_x, origin_y):
    #print('spitfire here')
    #print(origin_x, origin_y)
    bullet1 = bullet.bullet(origin_x, origin_y, 5, weapon_images_path.joinpath('spitfire.png'), angle = 0)
    #bullet1 = movement.Move(bullet1).__left__()

    behaviorArray = ["down"]
    moveCountArray = [80]
    speedArray = [10]
    #return movement.Move(behaviorArray,moveCountArray,speedArray)
    return bullet1

def spitfire3(origin_x, origin_y):
    #print('spitfire here')
    #print(origin_x, origin_y)
    bullet1 = bullet.bullet(origin_x, origin_y, 5, weapon_images_path.joinpath('spitfire.png'), angle = 1)
    bullet2 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = -1, behavior='northEast')
    bullet3 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = 0, behavior='northNorthEast')
    bullet4 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = 2, behavior='northWest')
    bullet5 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = -2, behavior='northNorthWest')

    return bullet1, bullet2, bullet3, bullet4, bullet5
    #self.weapon.weapon_func()
    #return bullet.bullet(origin_x, origin_y, 5, self.weapon.weapon_image)
    #player_bullet_sprites.add(bullet1)

def spitfire2(origin_x, origin_y):
    #print('spitfire here')
    #print(origin_x, origin_y)
    bullet1 = bullet.bullet(origin_x, origin_y, 5, weapon_images_path.joinpath('spitfire.png'), angle = 1)
    bullet2 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = -1, behavior='northNorthEast')
    bullet3 = bullet.bullet(origin_x + 5, origin_y + 5, 5, weapon_images_path.joinpath('spitfire.png'), angle = 0, behavior='northNorthWest')
    return bullet1, bullet2, bullet3

def blue_lazer(origin_x, origin_y):
    bullet1 = bullet.bullet(origin_x, origin_y, 5, weapon_images_path.joinpath('blue_lazer.gif'), angle = 0)
    return bullet1

master_weapons_dict = {
    'spitfire': (10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire),
    'spitfire2': (10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire2),
    'spitfire3': (10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire3),
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


