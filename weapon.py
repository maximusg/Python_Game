'''
File: weapon.py
01/29/19
'''


'''
MASTER WEAPONS DICTIONARY

Tuple Index:         |       0       |       1          |       2          |       3          |
Description:         | BULLET DAMAGE | BULLET FIRE RATE | IMAGE PATH       | Speed            |
Units:               | 0-100 hp      | bullets per sec  | pathlib          | pixels/frame     |
                     |               |                  |                  |
-----------------------------------------------------------------------------------------------
    WEAPON NAME      | BULLET DAMAGE | BULLET FIRE RATE | IMAGE PATH       | Speed            |
                     |               |                  |                  |                  |
   spitfire          |       10      |       4          |       n/a        |       15         |
   blue_lazer        |       10      |       4          |       n/a        |       n/a        |

'''

import Entity
from library import*

#constants
spitfire_spread = 15
spitfire_offset = 5

#dictionary containing all in game weapons and their properties
#each weapon name will be mapped to its function, an image, and other properties

master_weapons_dict = dict(
    spitfire=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'),15),
    spitfire2=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), 15),
    spitfire3=(1, 15, WEAPON_IMAGES_PATH.joinpath('spitfire.png'), 15),
    blue_lazer=(1, 4, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), 15),
    master_lazer=(10, 60, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), 15),
    missle=(10, 5, WEAPON_IMAGES_PATH.joinpath('blue_lazer.gif'), 5),
    bomb=(30, 5, WEAPON_IMAGES_PATH.joinpath('bomb.png'), 5),
    waveBeam=(4, 2, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), 10),
    waveBeam2=(8, 3, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), 10),
    waveBeam3=(10, 4, WEAPON_IMAGES_PATH.joinpath('waveBeam_new_s.png'), 10),
    chargeShot= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot.png'), 10, 1),
    chargeShot2= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot.png'), 10, 2),
    chargeShot3= (1, 30, WEAPON_IMAGES_PATH.joinpath('chargeShot.png'), 10, 3)
                          )


class Weapon(object):
    '''
    The Weapon class is intended to be used by the Player class as well as the Enemy class.
    It will interact with the master_weapons_dict in order to give GUI the information it needs so
    that Bullet sprites can be constructed. Weapon also controls access to the bomb weapon function.
    '''

    def __init__(self, weaponName):
        #constructs a weapon as long as the supplied -weaponName is a valid weapon name (check the master_weapons_dict)
        if weaponName not in master_weapons_dict:
            raise RuntimeError('the weapon must be in the master weapons dictionary. you tried', weaponName)
        self.name = weaponName

        if not isinstance(master_weapons_dict.get(weaponName)[0], int):
            raise TypeError('bad weapon damage entry in master weapons dict. should be int')
        self.weapon_damage = master_weapons_dict.get(weaponName)[0]

        if not isinstance(master_weapons_dict.get(weaponName)[1], int):
            raise TypeError('bad rate of fire entry in master weapons dict. should be int')
        self.rof = master_weapons_dict.get(weaponName)[1] # rof is the rate of fire in bullets per second

        if not isinstance(master_weapons_dict.get(weaponName)[2], Path):
            raise TypeError('bad image path entry in master weapons dict. should be Path (pathlib)')
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
        if weaponName not in self.weapon_fire_dic:
            raise RuntimeError('the weapon must be in the weapon_fire_dic')
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

    #getters
    def getDamage(self, name):
        #returns the damage of a weapon, -name must be a valid weapon name
        return master_weapons_dict.get(name)[0]
    def getImagePath(self, name):
        #returns the image path of a weapon, -name must be a valid weapon name
        return master_weapons_dict.get(name)[2]
    def getSpeed(self, name):
        #returns the speed of a weapon, -name must be a valid weapon name
        return master_weapons_dict.get(name)[3]

    #weapon functions, makes bullets for GUI, called when playerShip fires(). All weapon functions require an origin_x and origin_y values for where the bullets are to appear in the game
    #origin_x and origin_y are typically derived from the playerShip's current position.
    def chargeShot(self, origin_x, origin_y):
        '''
        chargeShot will "charge" (increment chargeShot timer) as the player holds down the fire key, and when the key is released
        a rapid stream of bullets will be shot continuosly until the chargeShot timer hits 0
        Leveling up this weapon will allow it to charge faster (increase the rate at which chargeShot timer increments)
        There is an animation that accompanies the chargeShot
        '''
        weapon = 'chargeShot'
        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), angle = 0, behavior='up', name = self.name, damage = self.weapon_damage)
        return bullet1

    def waveBeam(self, origin_x, origin_y):
        '''
        waveBeam will shoot an expanding wave that deals high damage to enemies
        Leveling up waveBeam will increase damage dealt as well as rof
        '''
        weapon = 'waveBeam'

        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), angle = 0, behavior='up', name = 'waveBeam', damage = self.weapon_damage)
        return bullet1

    def spitfire(self, origin_x, origin_y):
        '''
        spitfire is meant to be a general purpose weapon, with a high rof but low damage
        Leveling up spitfire will cause additional spitfire Bullets to fire at enemies
        '''
        weapon = 'spitfire'

        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), angle = 0, behavior='up', damage = self.weapon_damage)


        return bullet1

    def spitfire3(self, origin_x, origin_y):
        '''
        spitfire is meant to be a general purpose weapon, with a high rof but low damage
        Leveling up spitfire will cause additional spitfire Bullets to fire at enemies
        '''
        weapon = 'spitfire3'


        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet2 = Entity.Bullet(origin_x - 2*spitfire_spread, origin_y + 3*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet3 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet4 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet5 = Entity.Bullet(origin_x + 2*spitfire_spread, origin_y + 3*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)

        return bullet1, bullet2, bullet3, bullet4, bullet5

    def spitfire2(self, origin_x, origin_y):
        '''
        spitfire is meant to be a general purpose weapon, with a high rof but low damage
        Leveling up spitfire will cause additional spitfire Bullets to fire at enemies
        '''
        weapon = 'spitfire2'


        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet2 = Entity.Bullet(origin_x - spitfire_spread, origin_y + 2*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        bullet3 = Entity.Bullet(origin_x + spitfire_spread, origin_y + 2*spitfire_offset, self.getSpeed(weapon), self.getImagePath(weapon), behavior='up', damage = self.weapon_damage)
        return bullet1, bullet2, bullet3

    def blue_lazer(self, origin_x, origin_y):
        '''
        blue_lazer is a starter weapon, similar in ability to level 1 spitfire
        '''
        weapon = 'blue_lazer'

        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), damage = self.weapon_damage)
        return bullet1

    def missle(self, origin_x, origin_y):
        '''
        missile is an experimental weapon that uses advanced Movement

        '''
        weapon = 'missle'

        bullet1 = Entity.Bullet(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), behavior="missle", damage = self.weapon_damage)
        return bullet1

    def bombs(self, origin_x, origin_y):
        '''
        bombs are not typical weapons, they have 2 stages: stage 1 is the launch, where the bomb travels up the screen
        If the bomb doesn't go off the edge of the screen during the launch stage,
        then it will explode (stage 2) dealing damage to all enemies on screen
        '''
        weapon = 'bomb'

        bomb1 = Entity.Bomb(origin_x, origin_y, self.getSpeed(weapon), self.getImagePath(weapon), behavior='bomb')
        return bomb1

#code for the chargeShot charging animations
cwd = Path.cwd()
charging_images_path = cwd.joinpath('resources', 'weapon_images', 'chargeShot', 'charging')
bomb_sounds = cwd.joinpath('resources', 'sound_effects', 'bomb_sounds')
#Constants
TOTAL_ANIM_FRAMES = 4

class ChargingAnim(pygame.sprite.Sprite):
    '''Sprite encapsulating the Charged Shot animation.'''
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
        '''Updates sprite based on whether the ship is still charging the weapon or not.'''
        #checks if the playerShip is still charging the weapon
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
        '''Moves the sprite rect by (diffx, diffy).'''
        #standard move function, moves the object's rect by an x and y differential
        self.rect = self.rect.move(diffx, diffy)

    def play_sound(self):
        #vestigial play_sound, in case we ever want to add a charging sound it's here
        self.sound.play()


#utility functions
def is_weapon(name):
    #simple function that is helpful to check whether a given name (string) is a weapon name
        if name in master_weapons_dict:
            return name
        else:
            return False


def upgrade(item_pickup, current_weapon):
    '''
    This is a helper function that is used when a player picks up an weapon Item powerup
    The Player can run this upgrade function to determine if they should get a new Weapon,
    and which one it is. In order to use it: -item_pickup must be an Item object that is a weapon powerup
    and -current_weapon will be the name of the playerShip's current weapon (easily found by weapon.name)
    '''
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


