import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os
import math
import random

import movement
import weapon
#import bullet
import itemDropTables
#import item_pickup
import explosion

from library import *
from levelLibrary import *

class Entity(pygame.sprite.Sprite):
    '''
    Entity is a broad class encompassing Enemies, the Player, Items, etc. All of these entities have certain characteristics
    such as a location given by -origin, an optional -imageFile that is used as the sprite image, an -acceleration, -speed, and -angle
    used in the case that the Entity's movement is governed by the Move class, a -health which indicates how much damage it can take before
    being destroyed, and a -point_value that indicates how much the Entity will increase the Player's score.
    '''
    def __init__(self, origin=(0,0), imageFile=None, area=None, acceleration=0,speed=0, angle=0, health=1, point_value=0):
        super().__init__()
        self.health = health
        self.screen = pygame.display.get_surface()
        self.speedX = math.sin(math.radians(angle))*speed
        self.speedY = math.cos(math.radians(angle))*speed
        self.speed = speed
        self.angle = angle
        self.rotation = 0
        self.acceleration = acceleration
        self.imageFile = imageFile
        self.image=None
        self.rect=None
        self.value = point_value
        self.visible = 1
        
        self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)

        #loading picture    
        if imageFile!=None:
            self.image, self.rect = ASSET_MANAGER.getAsset(imageFile)
        else:#if no image give creates a 20X20 red square.
            self.image = pygame.Surface([20, 20])
            self.image.fill(RED)
            self.rect = self.image.get_rect()
        self.rect.x = origin[0]
        self.rect.y = origin[1]

    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, value):
        if not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid int for health.')
        self.__health = value

    @property
    def angle(self):
        return self.__angle
    
    @angle.setter
    def angle(self, value):#speed comes before angel so need to check if it exists like speed chesk for angle
        if not isinstance(value, int) and not isinstance(value,float):
            raise RuntimeError(value + ' is not a valid int for angle.')
        value = value%360
        self.speedX = math.sin(math.radians(value))*self.speed
        self.speedY = math.cos(math.radians(value))*self.speed

        self.__angle = value

    @property
    def rotation(self):
        return self.__rotation
    
    @rotation.setter
    def rotation(self, value):#speed comes before angel so need to check if it exists like speed chesk for angle
        if not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid int for angle.')
        value = value%360
        self.__rotation = value

    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self, value):
        if not isinstance(value, int) and not isinstance(value,float):
            raise RuntimeError(value + ' is not a valid int for speed.')
        try :
            self.angle #checks for the first case when angle is being contructed
        except: 
            self.__speed = value
        else:
            self.speedX = math.sin(math.radians(self.angle))*value
            self.speedY = math.cos(math.radians(self.angle))*value
            self.__speed = value

    @property
    def acceleration(self):
        return self.__acceleration
    
    @acceleration.setter
    def acceleration(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise RuntimeError(value + ' is not a valid float for acceleration.')
        self.__acceleration = value

    def updateSpeed(self):
        '''Updates self.speedX and self.speedY based on angle and acceleration.'''        
        self.speedX += math.sin(math.radians(self.angle))*self.acceleration 
        self.speedY += math.cos(math.radians(self.angle))*self.acceleration
        
    
    def move(self, x, y):#keeps object from going past the  sides
        '''Updates the Entity's rect location while ensuring it remains within the window.'''
        if self.rect.left < self.area.left: 
            self.rect.left = self.area.left
            self.speedX = -self.speedX
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
            self.speedX = -self.speedX
        else:
            self.rect = self.rect.move((x, y))

    def update(self):
        '''If not inside the window area, mark for removal.'''
        if not self.area.colliderect(self.rect):
            self.visible = 0
            
class Player(Entity):
    '''
    The Player Class inherits from Entity, and extends it by adding an -init_wep which is the Player's
    initial Weapon object, -scheme which is the control scheme (keyboard controls), -init_bomb which is a special
    Weapon object.
    '''
    def __init__(self, init_wep, imgFile, scheme, init_bomb = 'bomb'):
        super().__init__(imageFile=MISC_SPRITES_PATH.joinpath(imgFile))
        self.weapon = weapon.Weapon(init_wep)

        self.bomb = weapon.Weapon(init_bomb)
        self.bombs_remaining = 3
        self.bomb_wait = False
        self.drop_bomb_flag = False
        self.curr_bomb = None

        self.control_scheme = scheme ##placeholder
        self.point_total = 0
        self.max_health = 40
        self.health = 40
        self.max_shield = 100
        self.shield = 100
        self.healthpack = 10 #this determines how much health is restored when picking up a healthpack
        # self.image, self.rect = load_image(imgFile, -1)
        self.invul_flag = False

        # self.area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)

        self.rect.center = PLAYER_START
        self.speed = 10
        self.bullet_count = 0

    def take_damage(self, value):
        '''
        When a Player is hurt, the take_damage function is used to decrease the player's health and shield
        '''
        if self.shield > 0:
            self.shield -= value*2
            if self.shield < 0:
                self.health -= int(abs(self.shield*0.5))
                self.shield = 0
        else:
            self.health -= value
            if self.health < 0:
                self.health = 0

    def regen(self):
        '''
        The regen method allows the Player's shield to regenerate as long as the current shield level is below the max shield attribute
        '''
        self.shield += 1
        if self.shield > self.max_shield:
            self.shield = 100

    def move(self, new_x, new_y):
        '''
        The move method allows the Player to move to a coordinates, given by -new_x and -new_y
        There is some bounds checking to ensure that the Player moves within the allowed area.
        '''
        if self.rect.left < self.area.left: ###I hate this function. I need to make it better. -Chris
            self.rect.left = self.area.left
        elif self.rect.right > self.area.right:
            self.rect.right = self.area.right
        elif self.rect.top < self.area.top:
            self.rect.top = self.area.top
        elif self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom
        else:
            self.rect = self.rect.move((new_x, new_y))

    def fire(self):
        '''
        The fire method calls on the Player's current Weapon object to return a Bullet. A Bullet contains all
        the necessary information for drawing a bullet sprite on the screen (GUI) as well as managing that sprite's
        movement and damage.
        '''
        origin_x = self.rect.centerx
        origin_y = self.rect.top

        return self.weapon.weapon_func(origin_x, origin_y)
        
    def drop_bomb(self):
        '''
        Similar to the fire method, the drop_bomb method allows the Player to launch a bomb Weapon object.
        Refer to the bomb documentation in weapon.py for more info about bombs.
        '''
        origin_x = self.rect.centerx
        origin_y = self.rect.top
        self.drop_bomb_flag = True
        self.bomb_wait = True

        return self.bomb.weapon_func(origin_x, origin_y)
    
    def control(self, keys, FRAMERATE):
        '''
        This method defines the control scheme used to move the Player in game
        '''
        addBullet=False
        if self.control_scheme=="arrows":
            if keys[pygame.K_UP]:
                self.move(0,-self.speed)
            if keys[pygame.K_DOWN]:
                self.move(0,self.speed)
            if keys[pygame.K_LEFT]:
                self.move(-self.speed, 0)
            if keys[pygame.K_RIGHT]:
                self.move(self.speed, 0)
            ##this if/else statement must stay together
            if keys[pygame.K_SPACE]:
                if self.bullet_count % (int(FRAMERATE/self.weapon.rof)) == 0:
                    addBullet=True
                self.bullet_count += 1
            else:
                self.bullet_count = 0
            ##end if/else
            if keys[pygame.K_b]:
                if self.bomb_wait == False and self.bombs_remaining > 0:
                    self.drop_bomb()
                    self.bombs_remaining -= 1
            ##end if/else    
            if DEBUG:
                if keys[pygame.K_1]:
                    self.weapon = weapon.Weapon('spitfire')
                if keys[pygame.K_2]:
                    self.weapon = weapon.Weapon('spitfire2')
                if keys[pygame.K_3]:
                    self.weapon = weapon.Weapon('spitfire3')
                if keys[pygame.K_4]:
                    self.weapon = weapon.Weapon('waveBeam')
                if keys[pygame.K_5]:
                    self.weapon = weapon.Weapon('waveBeam2')
                if keys[pygame.K_6]:
                    self.weapon = weapon.Weapon('waveBeam3')
                if keys[pygame.K_7]:
                    self.weapon = weapon.Weapon('chargeShot')
                if keys[pygame.K_8]:
                    self.weapon = weapon.Weapon('chargeShot2')
                if keys[pygame.K_9]:
                    self.weapon = weapon.Weapon('chargeShot3')
        return addBullet

    def update(self):
        '''Generate explosions based on health on a per frame basis.'''
        if 0.75 < self.health / self.max_health <= 0.9:
            if random.random() < 0.01:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        elif 0.3 < self.health / self.max_health <= 0.75:
            if random.random() < 0.05:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        elif 0 <= self.health / self.max_health <= 0.3:
            if random.random() < 0.15:
                x = random.randint(self.rect.left,self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                return explosion.ExplosionSprite(x,y)
        else:
            return None
            
class Enemy(Entity):
    '''
    The Enemy class is similar to the Player class, but with several key differences. While both Player and Enemy extend
    the Entity class, Player has a control scheme that allows the player to control the ship, while Enemy's execute
    pre-set behavior, found in the behaveDic. Additionally, the game screen has been divided into sectors, and enemies may
    appear from any of the allowed sectors, giving them their origin. Finally, when enemies are defeated, they may drop Items to pickup, as specified by their itemDropTable.
    For more information on item drops, see itemDropTables.py

    '''
    def __init__(self, origin=ENEMY_SECTORS("s4"), imgFile="enemy.png", speed=1, behavior="diver", weapon="spitfire", health=1, acceleration=0, itemDropTable = itemDropTables.common, angle=0):
        imgFile = MISC_SPRITES_PATH.joinpath('enemy'+str(ENEMY_SPRITE[behavior])+'.png') #selects the sprite skin based off behavior
        area = pygame.Rect(COLUMN_WIDTH, 0, SCREEN_WIDTH-(2*COLUMN_WIDTH), SCREEN_HEIGHT)

        super().__init__(origin=origin, imageFile=imgFile, area=area, speed=speed, acceleration=acceleration, angle=angle, health=health, point_value=ENEMY_VALUE)
        self.weapon = weapon
        # self.point_value = 500
        self.behaveDic = {
        	"diver":self.__diver__, 
        	"camper":self.__camper__, 
        	"sleeper":self.__sleeper__,
        	"crazy":self.__crazy__,
        	"crazyReverse": self.__crazyReverse__,
        	"mrVectors": self.__mrVectors__,
        	"diveBomb": self.__diveBomb__,
        	"diveStrafe": self.__diveStrafe__
        	}
        self.movement = self.behaveDic[behavior]()
        self.itemDropTable = itemDropTable

    #behavior method
    def __diver__(self):
        down=["x","x",0]
        right=["x","x",90]
        vectorArray = [down,right]
        moveCountArray = [130,50]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=2)

    #behavior method
    def __camper__(self):
        down=["x","x",0]
        left=["x","x",-90]
        vectorArray = [down,left]
        moveCountArray = [130,50]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=3)

    #behavior method
    def __crazy__(self):
        
        down =["x","x",0]#comes down at spawn speed
        left = ["x","x",-90]
        right = ["x","x",90]
        up = ["x","x",180]
        northWest = ["x","x",180-46]
        northEast =["x","x", 180+46]
        southWest = ["x","x",-46]
        southEast =["x","x", 46]
        

        moveCountArray = [5,	15,	25,	10,   10,  10,20,25,5,20,25]
        vectorArray = [down, left, right, left, up, down, northWest,southEast,down,northEast,southWest]
        
        return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

    #behavior method
    def __crazyReverse__(self):
        down =["x","x",0]#comes down at spawn speed
        left = ["x","x",-90]
        right = ["x","x",90]
        up = ["x","x",180]
        northWest = ["x","x",180-46]
        northEast =["x","x", 180+46]
        southWest = ["x","x",-46]
        southEast =["x","x", 46]
        
        
        moveCountArray = [25,20,5,25,20,10,10,10,25,15,5]
        vectorArray = [southWest,northEast,down,southEast,northWest,down,up,left,right,left,down]
        return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=3)

    #behavior method
    def __sleeper__(self):# moves down and stops for a LLLONG time =, the wiggles left and right FAST, the stops again, the dives down
        behaviorArray = ["down","stop","left","right"]
        down =["x","x",0]#comes down at spawn speed
        stop = [0,0,0]
        left = [0,3,-90]
        right = ["x","x",90]
        moveCountArray = [50,	20,	10,		10]
        vectorArray = [down,stop,left,right]
        return movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=1)

    #behavior method
    def __mrVectors__(self): #EXAMPLE for vector movements
        #vector = [acceleration, speed, angle] if there is an "x" 
        # you will use the entities default, which if not set is 0.

        #couple of examples
        
        southWest1 = [3,"x",-85]
        southEast1 =["x","x", 85] 
        southWest2 = ["x","x",-65]
        southEast2 =["x","x", 65] 
        southWest3 = ["x","x",-50]
        southEast3 =["x","x", 50] 
        southWest4 = ["x","x",-30]
        southEast4 =[0,"x", 30] 
        

        #fill the vector array to execute each moveCount
        vectorArray = [ southWest1, southEast1, southWest2, southEast2, southWest3,southEast3, southWest4,southEast4]
        #still uses frame count
        moveCountArray = [20,20,  15, 15,  10, 10, 5, 5]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=3)

    #behavior method
    ##NEW##
    def __diveBomb__(self):
        dive=["x","x","x"]
        return movement.Move(moveCountArray=[100000],vectorAray=[dive])

    #behavior method
    ##NEW##
    def __diveStrafe__(self):
    
        diveLeft=["x","x",45]
        diveRight=["x","x",-45]

        return movement.Move(moveCountArray=[25,25],vectorAray=[diveLeft,diveRight],repeat=10)

    def update(self):
        '''
        During the main game loop, the enemy sprites are updated. They may shoot bullets at the player by random chance.
        '''
        # self=self.movement.update(self)
        bullet_to_add = []
        self.movement.update(self)
        super().update()
        
        if self.visible:
            if random.random() <= 0.01:
                bullet_to_add.append(Bullet(self.rect.centerx, self.rect.centery, 20, 'resources/weapon_images/spitfire.png', behavior='down'))
        return bullet_to_add

    def getDrop(self):
        '''
        When an enemy's health reaches 0, it is defeated and has a chance to drop items. The
        getDrop method calculates which Item, if any, is created on screen. See itemDropTables.py for more info.

        '''
        #build the working drop table
        item_lower_threshold = []
        item_upper_threshold = []
        total_probability = 0
        rand_num = random.random() #pulls a random number between 0 and 1

        #index = 0

        #returns None if no drop table
        if self.itemDropTable is None:
            return None

        #this part deals with itemDropTables that just have 1 item
        if len(self.itemDropTable) == 2:
            if rand_num < self.itemDropTable[1]:
                return Item(self.rect.centerx, self.rect.centery, name= self.itemDropTable[0])

        #this part deals with itemDropTables that have multiple items
        else:
            index = 0
            for item in self.itemDropTable:
                item_lower_threshold.append(total_probability)
                item_upper_threshold.append(total_probability + item[1])
                total_probability += item[1]
                if rand_num > item_lower_threshold[index] and (rand_num <= item_upper_threshold[index]):
                    return Item(self.rect.centerx, self.rect.centery, name= item[0])
                index += 1
        return None

    def take_damage(self, value):
        '''
        health is lowered by -value.
        '''
        self.health -= value
        if self.health <= 0:
            self.visible = 0

class Bullet(Entity):
    '''
    Bullets are entities that appear in a position given by -origin_x, -origin_y (typically the playerShip)
    then, they travel with a behavior given by -speed, -acceleration, -angle, -behavior. The name of the bullet is
    relevant in certain special cases where the GUI needs to make decisions on certain bullet types, so -name is used to pass
    the name of the Bullet in from Weapon in this scenario. Finally, bullets deal -damage on collision.
    '''

    def __init__(self, origin_x, origin_y, speed, path_to_img, acceleration=0, angle = 0, behavior = 'up', name = None, damage = 1):
        location = (origin_x, origin_y)
        super().__init__(origin=location, imageFile=path_to_img, speed=speed, acceleration=acceleration, angle=angle )

        # self.dirty = 1
        # self.mask = pygame.mask.from_surface(self.image)
        self.name = name

        #in order to reuse in other methods.
        self.NE = ["x", self.speed*0.5 ,(180+30)]
        self.NNE = ["x", self.speed*0.5 ,(180+15)]
        self.NW = ["x", self.speed*0.5 ,(180-30)]
        self.NNW = ["x", self.speed*0.5 ,(180-15)]


        self.behaveDic = {
        	"up":self.__up__,
        	"northWest":self.__northWest__,
        	"northEast":self.__northEast__,
        	"northNorthEast":self.__northNorthEast__,
        	"northNorthWest":self.__northNorthWest__,
        	"missle":self.__missleLeft__,
        	"down":self.__down__,
        	"vector":self.__vector__
        	}

        self.movement = self.behaveDic[behavior]()
        self.damage = damage


    def move(self, x, y):
        #simple movement method, moves the Bullet's rect by x and y
        self.rect = self.rect.move((x, y))


    def update(self):
        '''
        Every frame, the bullet has to move. This is handled here in the update method.
        In the case that the name of the bullet is waveBeam, it will expand as it moves, so that is handled here.
        '''
        if self.name == "waveBeam":
            wave_growth = 2
            wave_size = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (int(wave_size[0]+wave_growth), int(wave_size[1])))
            self.rect = self.rect.inflate(wave_growth, 0)
        super().update()
        self.movement.update(self)

    #behavior methods
    def __up__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[BULLET_VECTORS['UP']] ) 

    def __northEast__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[self.NE]) 

    def __northNorthEast__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[self.NNE])  

    def __northWest__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[self.NW]) 

    def __northNorthWest__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[self.NNW]) 

    def __missleLeft__(self):
        accelerateUp = [2,"x",180] #sets acceleration to 2
        moveCountArray = [5,1,800]
        return movement.Move(moveCountArray=moveCountArray, vectorAray=[[self.NW],accelerateUp,DEFAULT]) #uses "DEFAULT"to keep the missle moving

    def __down__(self):
        return movement.Move(moveCountArray=[800], vectorAray=[BULLET_VECTORS['DOWN']] ) 

    def __vector__(self):
        vector = ["x",self.speed,self.angle]
        return movement.Move(moveCountArray=[1000],vectorAray=[vector])


class Item(Entity):
    '''
    The Item class represents items that are dropped by defeated enemies, and which the player can collect.
    Some items will give the player points, increasing the player's score, while other items are weapon powerups,
    granting the player a new weapon or improving the player's existing weapon. Additional items include healthpacks
    which restore health, as well as bomb items which increase the number of bombs the player can drop by 1.
    All items can be found in the MASTER_ITEMS dictionary in "library.py"
    '''
    def __init__(self, origin_x, origin_y, speed = 1, path_to_img = 'powerup.gif', name = None):
        self.weapon_name = None
        if name is not None:
            if name in MASTER_ITEMS:
                path_to_img = ITEM_IMAGES_PATH.joinpath(MASTER_ITEMS.get(name)[0])
                weapon_name = MASTER_ITEMS.get(name)[1]
                self.is_weapon = weapon.is_weapon(weapon_name)
                if self.is_weapon:
                    self.weapon_name = self.is_weapon
        
        super().__init__(origin=(origin_x,origin_y), imageFile=ITEM_IMAGES_PATH.joinpath(path_to_img), speed=speed, point_value=ITEM_VALUE)
        self.name = name


    def checkWeapon(self):
        '''helper method that checks if the Item is a weapon powerup.'''
        if self.weapon_name is not None:
            return True

        return False

    def checkBomb(self):
        '''helper method that checks if the Item is a bomb item.'''
        if self.name in MASTER_ITEMS:
            if self.name is 'bomb_item':
                return True

        return False

    def checkHealthPack(self):
        '''helper method that checks if the Item is a health pack, giving the player back health (red) not shield (blue).'''
        if self.name in MASTER_ITEMS:
            if self.name is 'healthpack':
                return True

        return False

    def move(self, x, y):
        '''simple move method that moves the Item by x and y pixels.'''
        self.rect = self.rect.move((x, y))

    def update(self):
        '''moves straight down at a given speed.'''
        super().update()
        self.move(0,self.speed)
        
class BossSprite(Entity):
    '''
    The BosoSprite is a special type of enemy that the player encounters at the end of a level.
    This powerful foe has much more health than the typical enemy, as well as a shield.

    '''
    def __init__(self, origin, path_to_img):
        super().__init__(origin=origin, imageFile=MISC_SPRITES_PATH.joinpath(path_to_img), point_value=BOSS_VALUE)
        # self.image, self.rect = load_image(path_to_img)
        self.shield_gen_loc = (10,10)
        # self.rect.x = origin[0]
        # self.rect.y = origin[1]
        self.launchers = ((250,150),(150,150),(50,150))

        self.point_value = 50000
        self.max_health = 150
        self.max_shield = 100

        self.health = self.max_health
        self.shield = self.max_shield
        self.regen_counter = 90

        self.phase = 1
        self.phase_counter = 300

        self.visible = 1

    def update(self, player_center):
        '''
        the BossSprite has a complex update method, due to the fact that there are multiple phases of combat behavior
        that the BossSprite executes during a battle with the player. As the BossSprite loses health, it will enter
        the next phase, leading to more powerful attacks.
        '''
        self.move()
        self.regen()

        explosion_list = []
        bullet_list = []

        ##set up explosions
        if self.shield == 0:
            if random.random() < 0.05:
                explosion_list.append(explosion.ExplosionSprite(self.rect.left + self.shield_gen_loc[0]+random.randint(-2,2), self.rect.top + self.shield_gen_loc[1]+random.randint(-2,2), 'up'))
        
        if 0.25 < self.health / self.max_health <= 0.5:
            if random.random() < 0.05:
                explosion_list.append(explosion.ExplosionSprite(random.randint(self.rect.left, self.rect.right), random.randint(self.rect.top, self.rect.bottom), 'up'))
        if 0 <= self.health / self.max_health <= 0.25:
            if random.random() < 0.15:
                explosion_list.append(explosion.ExplosionSprite(random.randint(self.rect.left, self.rect.right), random.randint(self.rect.top, self.rect.bottom), 'up'))
        
        #set up bullets
        if self.phase == 1:
            if random.random() < 0.05:
                bullet_list.append(Bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
                bullet_list.append(Bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
                bullet_list.append(Bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
            self.phase_counter -= 1
            if self.phase_counter == 0:
                self.phase_counter = 600
                self.phase = 2
        elif self.phase == 2:
            if random.random() < 0.1:
                if player_center[1] > self.rect.bottom:
                    delta_x = (self.rect.x+self.launchers[0][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(Bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', 0, angle, 'vector'))

                    delta_x = (self.rect.x+self.launchers[1][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(Bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', 0, angle, 'vector'))

                    delta_x = (self.rect.x+self.launchers[2][0])-player_center[0]
                    delta_y = self.rect.bottom - player_center[1]
                    angle = math.degrees(math.atan(delta_x/delta_y))
                    bullet_list.append(Bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', 0, angle, 'vector'))
                else:
                    bullet_list.append(Bullet(self.rect.x+self.launchers[0][0], self.rect.y+self.launchers[0][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
                    bullet_list.append(Bullet(self.rect.x+self.launchers[1][0], self.rect.y+self.launchers[1][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
                    bullet_list.append(Bullet(self.rect.x+self.launchers[2][0], self.rect.y+self.launchers[2][1], 5, 'resources/weapon_images/spitfire.png', 0, random.randint(-45,45),'vector'))
            self.phase_counter -= 1
        
        return explosion_list, bullet_list
        

    def move(self):
        '''The BossSprite will move differently depending on which phase it is currently in.'''
        if self.phase == 1:
            if self.rect.y < 300:
                self.rect = self.rect.move(0,3)
            else:
                self.rect = self.rect.move(random.randint(-2,2), random.randint(-2,2))
        elif self.phase == 2:
            if self.rect.y > 100:
                self.rect = self.rect.move(random.randint(-5,5),-5)
            else:
                self.rect = self.rect.move(random.randint(-2,2),0)


    def regen(self):
        '''
        If the BossSprite has shield remaining, (shield > 0), then it will regenerate shield much like the Player
        '''
        if self.regen_counter == 0:
            if 0 < self.shield < self.max_shield:
                self.shield += 1
                self.regen_counter = 90
        else:
            self.regen_counter -= 1
            

    def take_damage(self, value):
        '''
        The BossSprite will take damage given by -value
        '''
        if self.shield > 0:
            self.shield -= value
            if self.shield < 0:
                self.shield = 0
        else:
            self.health -= value
            if self.health < 0:
                self.health = 0
        if self.health <= 0:
            self.visible = 0
        
class Bomb(Entity):
    '''
    The Bomb class represents stage 1 of the bomb. During this stage, the bomb is launched by the player, and travels
    up the screen with a Movement behavior defined by -behavior, -speed, -angle. The bomb appears at -origin_x, -origin_y
    typically near the playerShip. During stage 1, the bomb travels up the screen and a bomb drop sound effect is played.
    '''
    def __init__(self, origin_x, origin_y, speed, path_to_img, angle=0, behavior='bomb'):
        super().__init__(origin=(origin_x, origin_y), imageFile=WEAPON_IMAGES_PATH.joinpath(path_to_img), speed=speed, angle=angle)
        self.off_screen = False

        self.sound = load_sound(str(BOMB_SOUND_PATH.joinpath('bomb_drop.ogg')))

        self.bomb_timer = 100
        self.bomb_explode = False
        
        self.behaveDic = {
            "bomb": self.__bomb__,
            "upSlow": self.__upSlow__

        }

        self.movement = self.behaveDic[behavior]()

    def play_sound(self):
        '''plays the bomb drop sound effect.'''
        self.sound.play()

    def update(self):
        '''if the bomb goes off the screen, it will be removed from the game. Try to launch your bombs with enough space for them to travel
        without going off the top of the screen.'''
        super().update()

        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.right > SCREEN_WIDTH - COLUMN_WIDTH or self.rect.left < COLUMN_WIDTH:  # checks if the rect is out of bounds, and if so, it is no longer visible, meaning it should be deleted by GUI
            self.visible = 0
            self.dirty = 1

        #new movement after bomb slows down to a threshold of speed 3. upSlow moves the bomb up slowly forever
        if self.speed <= 3:
            self.movement = self.__upSlow__()

        self.bomb_timer -= 1
        if self.bomb_timer <= 0 and self.visible == 1:
            self.visible = 0
            self.bomb_explode = True
            self.centerx= self.rect.x
            self.centery = self.rect.y
        self.movement.update(self)

    #bomb movement behavior methods
    def __upSlow__(self):
        moveCountArray = [3000]
        vectorArray = [[0, 2, 180]]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=99)

    def __bomb__(self):
        moveCountArray = [1,100]
        vectorArray = [[0, 15, 180],[-.18, "x", "x"]]
        return movement.Move(moveCountArray=moveCountArray,vectorAray=vectorArray, repeat=99)
