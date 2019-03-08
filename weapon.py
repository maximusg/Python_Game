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

from pathlib import Path
import Entity
#import bomb

# cwd = Path.cwd()
# weapon_images_path = cwd.joinpath('resources', 'weapon_images')
weapon_images_path = Path('resources/weapon_images')

spitfire_spread = 15
spitfire_offset = 5
#each weapon name will be mapped to its function, an image, and other properties

def waveBeam(origin_x, origin_y):
    bullet1 = Entity.Bullet(origin_x, origin_y, 10, weapon_images_path.joinpath('waveBeam_new_s.png'), angle = 0, behavior='up', name = 'waveBeam')
    return bullet1

def spitfire(origin_x, origin_y):
    #print('spitfire here')
    #print(origin_x, origin_y)
    bullet1 = Entity.Bullet(origin_x, origin_y, 15, weapon_images_path.joinpath('spitfire.png'), angle = 0, behavior='up')


    return bullet1

def spitfire3(origin_x, origin_y):
    #print('spitfire here')
    #print(origin_x, origin_y)
    bullet1 = Entity.Bullet(origin_x, origin_y, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet2 = Entity.Bullet(origin_x - 2*spitfire_spread, origin_y + 3*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet3 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet4 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet5 = Entity.Bullet(origin_x + 2*spitfire_spread, origin_y + 3*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')

    return bullet1, bullet2, bullet3, bullet4, bullet5

def spitfire2(origin_x, origin_y):
    bullet1 = Entity.Bullet(origin_x, origin_y, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet2 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    bullet3 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, 15, weapon_images_path.joinpath('spitfire.png'), behavior='up')
    return bullet1, bullet2, bullet3

def blue_lazer(origin_x, origin_y):
    bullet1 = Entity.Bullet(origin_x, origin_y, 15, weapon_images_path.joinpath('blue_lazer.gif'))
    return bullet1

def missle(origin_x, origin_y):
    bullet1 = Entity.Bullet(origin_x, origin_y, 5, weapon_images_path.joinpath('blue_lazer.gif'), behavior="missle")
    return bullet1

def bombs(origin_x, origin_y):
    bomb1 = Entity.Bomb(origin_x, origin_y, 5, weapon_images_path.joinpath('bomb.png'), behavior='bomb')
    return bomb1

# def waveBeam(origin_x, origin_y):
#     bullet1 = Entity.Bullet(origin_x, origin_y, 15, weapon_images_path.joinpath('waveBeam.png'))
#     return bullet1

master_weapons_dict = dict(
    spitfire=(10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire),
    spitfire2=(10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire2),
    spitfire3=(10, 15, weapon_images_path.joinpath('spitfire.png'), spitfire3),
    blue_lazer=(10, 4, weapon_images_path.joinpath('blue_lazer.gif'), blue_lazer),
    master_lazer=(10, 60, weapon_images_path.joinpath('blue_lazer.gif'), blue_lazer),
    missle=(10, 5, weapon_images_path.joinpath('blue_lazer.gif'), missle),
    bomb=(10, 5, weapon_images_path.joinpath('bomb.png'), bombs),
    waveBeam=(10, 2, weapon_images_path.joinpath('waveBeam_new_s.png'), waveBeam),
    waveBeam2=(10, 3, weapon_images_path.joinpath('waveBeam_new_s.png'), waveBeam),
    waveBeam3=(10, 4, weapon_images_path.joinpath('waveBeam_new_s.png'), waveBeam),

                           )


class Weapon(object):

    def __init__(self, weaponName):

        if weaponName not in master_weapons_dict:
            raise Exception('the weapon must be in the master weapons dictionary. you tried', weaponName)
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



#utility functions
def is_weapon(name):
        if name in master_weapons_dict:
            return name
        else:
            return False

def upgrade(item_pickup, current_weapon):
    if item_pickup in master_weapons_dict:
        if item_pickup == 'spitfire':
            if current_weapon == 'spitfire':
                return 'spitfire2'
            elif current_weapon == 'spitfire2':
                return 'spitfire3'
            elif current_weapon == 'spitfire3':
                return 'spitfire3'
            else:
                return 'spitfire'
        if item_pickup == 'waveBeam':
            if current_weapon == 'waveBeam':
                return 'waveBeam2'
            elif current_weapon == 'waveBeam2':
                return 'waveBeam3'
            elif current_weapon == 'waveBeam3':
                return 'waveBeam3'
            else:
                return 'waveBeam'
    else:
        return None

if __name__=="__main__":
    def test():

        testWeapon = Weapon('spitfire')
        testWeapon2 = Weapon('blue_lazer')
        #os.startfile(testWeapon2.weapon_image)
        testWeapon.weapon_func()
    test()


