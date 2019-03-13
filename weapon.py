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

import Entity
from library import*

spitfire_spread = 15
spitfire_offset = 5
#each weapon name will be mapped to its function, an image, and other properties

master_weapons_dict = dict(
    spitfire=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'),None),
    spitfire2=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), None),
    spitfire3=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), None),
    blue_lazer=(1, 4, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), None),
    master_lazer=(10, 60, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), None),
    missle=(10, 5, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), None),
    bomb=(30, 5, WEAPON_IMAGES_PATH.joinpath('bomb.png'), None),
    waveBeam=(4, 2, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), None),
    waveBeam2=(8, 3, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), None),
    waveBeam3=(10, 4, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), None),
    chargeShot= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot','chargeShot.png'), None, 1),
    chargeShot2= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot','chargeShot.png'), None, 2),
    chargeShot3= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot','chargeShot.png'), None, 3)
                          )



# def waveBeam(origin_x, origin_y):
#     bullet1 = Entity.Bullet(origin_x, origin_y, 15, WEAPON_IMAGES_PATH.joinpath('waveBeam.png'))
#     return bullet1



class Weapon(object):

    def __init__(self, weaponName):

        if weaponName not in master_weapons_dict:
            raise Exception('the weapon must be in the master weapons dictionary. you tried', weaponName)
        self.name = weaponName
        self.weapon_damage = master_weapons_dict.get(weaponName)[0]

        self.rof = master_weapons_dict.get(weaponName)[1] # rof is the rate of fire in bullets per second
        self.weapon_image = master_weapons_dict.get(weaponName)[2]
        self.weapon_fire_dic =dict(
                                    spitfire=self.spitfire,
                                    spitfire2=self.spitfire2,
                                    spitfire3=self.spitfire3,
                                    blue_lazer=self.blue_lazer,
                                    master_lazer=self.blue_lazer,
                                    missle=self.missle,
                                    bomb=self.bombs,
                                    waveBeam=self.waveBeam,
                                    waveBeam2=self.waveBeam,
                                    waveBeam3=self.waveBeam,
                                    chargeShot=self.chargeShot,
                                    chargeShot2=self.chargeShot,
                                    chargeShot3=self.chargeShot,
                                    )
        self.weapon_func = self.weapon_fire_dic.get(weaponName)

        self.chargeShot_counter = 0
        self.chargeShot_counter_max = 100
        self.chargeShot_charging_flag = False
        self.chargeShot_firing_flag = False
        self.chargeShot_anim_visible = False
        self.chargeShot_dic = {
            'chargeShot':1,
            'chargeShot2':2,
            'chargeShot3':3
        }
        self.chargeShot_counter_rate = 1
        if self.name in self.chargeShot_dic:
            self.chargeShot_counter_rate = self.chargeShot_dic.get(self.name)
       # print(self.chargeShot_counter_rate)

    def getDamage(self, name):
        return master_weapons_dict.get(name)[0]

    def chargeShot(self, origin_x, origin_y):


        bullet1 = Entity.Bullet(origin_x, origin_y, 10, WEAPON_IMAGES_PATH.joinpath('chargeShot.png'), angle = 0, behavior='up', name = self.name, damage = self.weapon_damage)
        return bullet1

    def waveBeam(self, origin_x, origin_y):
        bullet1 = Entity.Bullet(origin_x, origin_y, 10, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), angle = 0, behavior='up', name = 'waveBeam', damage = self.weapon_damage)
        return bullet1

    def spitfire(self, origin_x, origin_y):
        #print('spitfire here')
        #print(origin_x, origin_y)
        bullet1 = Entity.Bullet(origin_x, origin_y, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), angle = 0, behavior='up', damage = self.weapon_damage)


        return bullet1

    def spitfire3(self, origin_x, origin_y):
        #print('spitfire here')
        #print(origin_x, origin_y)
        bullet1 = Entity.Bullet(origin_x, origin_y, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet2 = Entity.Bullet(origin_x - 2*spitfire_spread, origin_y + 3*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet3 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet4 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet5 = Entity.Bullet(origin_x + 2*spitfire_spread, origin_y + 3*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)

        return bullet1, bullet2, bullet3, bullet4, bullet5

    def spitfire2(self, origin_x, origin_y):
        bullet1 = Entity.Bullet(origin_x, origin_y, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet2 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        bullet3 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), behavior='up', damage = self.weapon_damage)
        return bullet1, bullet2, bullet3

    def blue_lazer(self, origin_x, origin_y):
        bullet1 = Entity.Bullet(origin_x, origin_y, 15, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), damage = self.weapon_damage)
        return bullet1

    def missle(self, origin_x, origin_y):
        bullet1 = Entity.Bullet(origin_x, origin_y, 5, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), behavior="missle", damage = self.weapon_damage)
        return bullet1

    def bombs(self, origin_x, origin_y):
        bomb1 = Entity.Bomb(origin_x, origin_y, 5, WEAPON_IMAGES_PATH.joinpath('bomb.png'), behavior='bomb')
        return bomb1


cwd = Path.cwd()
charging_images_path = cwd.joinpath('resources', 'weapon_images', 'chargeShot', 'charging')
bomb_sounds = cwd.joinpath('resources', 'sound_effects', 'bomb_sounds')
#Constants
TOTAL_ANIM_FRAMES = 4

class ChargingAnim(pygame.sprite.Sprite):
    def __init__(self, startx, starty, playerShip):
        super().__init__()
        anim0 = charging_images_path.joinpath('charging0.png')
        self.image, self.rect = ASSET_MANAGER.getAsset(str(anim0))
        self.rect = pygame.Rect(playerShip.rect.centerx,playerShip.rect.centery-60,30,30)

        #self.sound = load_sound(str(bomb_sounds.joinpath('Mboom.wav ')))
        self.frame_counter = 45
        self.frame = 1
        self.visible = 1
        self.playerShip = playerShip
        self.max_charging_width = 125
        self.max_charging_height = 135
        self.charge_grow = self.playerShip.weapon.chargeShot_dic.get(self.playerShip.weapon.name)
        self.charge_shrink = 2 #self.playerShip.weapon.chargeShot_dic.get(self.playerShip.weapon.name) * 2



    def update(self):
        if self.playerShip.weapon.chargeShot_charging_flag is False: #or self.frame_counter == 0:
            if self.playerShip.weapon.chargeShot_counter <= 0:
                self.visible = 0
                self.playerShip.weapon.chargeShot_anim_visible = False
            if self.playerShip.health <= 0:
                self.visible = 0
            if self.playerShip is None:
                self.visible = 0


        if self.playerShip.weapon.chargeShot_firing_flag is False:
            charging_size = self.image.get_size()
            #print(charging_size)
            self.frame += 1
            old_x, old_y = self.playerShip.rect.centerx, self.playerShip.rect.centery-60
            self.image, self.rect = ASSET_MANAGER.getAsset(str(charging_images_path.joinpath('charging')) + str(self.frame % TOTAL_ANIM_FRAMES)+'.png')
            self.rect.centerx, self.rect.centery = old_x, old_y
            if charging_size[0] < self.max_charging_width:
                self.image = pygame.transform.scale(self.image, (charging_size[0] + self.charge_grow, charging_size[1] + self.charge_grow))
                self.rect = self.image.get_rect(center=(old_x,old_y))
            else:
                self.image = pygame.transform.scale(self.image, (self.max_charging_width, self.max_charging_height))
                self.rect = self.image.get_rect(center=(old_x,old_y))
        else:
            charging_size = self.image.get_size()
           # print(charging_size)

            self.frame += 1
            old_x, old_y = self.playerShip.rect.centerx, self.playerShip.rect.centery-60
            self.image, self.rect = ASSET_MANAGER.getAsset(str(charging_images_path.joinpath('charging')) + str(self.frame % TOTAL_ANIM_FRAMES)+'.png')
            self.rect.centerx, self.rect.centery = old_x, old_y

            if (charging_size[0] - self.charge_shrink > 0) and (charging_size[1] - self.charge_shrink):
                self.image = pygame.transform.scale(self.image, (charging_size[0] - self.charge_shrink, charging_size[1] - self.charge_shrink))
                self.rect = self.image.get_rect(center=(old_x,old_y))
            else:
                self.image = pygame.transform.scale(self.image, (0, 0))
                self.rect = self.image.get_rect(center=(old_x,old_y))



    def move(self, diffx, diffy):
        self.rect = self.rect.move(diffx, diffy)

    def play_sound(self):
        self.sound.play()


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
        if item_pickup == 'chargeShot':
            if current_weapon == 'chargeShot':
                return 'chargeShot2'
            elif current_weapon == 'chargeShot2':
                return 'chargeShot3'
            elif current_weapon == 'chargeShot3':
                return 'chargeShot3'
            return 'chargeShot'
    else:
        return None

if __name__=="__main__":
    def test():

        testWeapon = Weapon('spitfire')
        testWeapon2 = Weapon('blue_lazer')
        #os.startfile(testWeapon2.weapon_image)
        testWeapon.weapon_func()
    test()


