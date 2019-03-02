
#!/bin/python
#this file will load files made by level loader, and retrun all the values in the format expected by the GUI,
#To not have to change the GUI's functionality to much, levelLoader is kind of like a helper class for GUI

import weapon
import player
import enemy
import bullet
from library import *
from levelLibrary import *
import json




class LevelLoader():
    def __init__(self, startingLevelNumber=1):
        self.levelNumber = startingLevelNumber
        # self.levelName = "level"+str(self.levelNumber)
        # self.levelPath = "levels/"+self.levelName+".json"
        self.level = None
        self.success = self.__levelLoad__()
       
        # self.PLAYER_TYPES = ["health", "location", "image"]
        # self.ENEMY_TYPES = ["class", "health"]
        # self.ENEMYBULLETS_TYPE = ["class"]

    @property
    def levelNumber(self):
        return self.__levelNumber

    @levelNumber.setter
    def levelNumber(self,number):
        self.__levelNumber = number
    
    @property
    def levelName(self):
        return "level"+str(self.levelNumber)

    @property
    def levelPath(self):
        return "levels/"+self.levelName+".json"


    @property
    def success(self):
        return self.__success
    @success.setter
    def success(self, tORf):
        self.__success = tORf
    
    # @property 
    # def DICTYPES(self):
    #     return self.__DICTYPES
    
    # @property
    # def TIMETYPES(self):
    #     return self.__TIME_TYPES
        
       

    def __levelLoad__(self):
        
        try:
            with open (self.levelPath,"r") as read_file:
                self.level= json.load(read_file)
        except FileNotFoundError as Error:
            return False
        except json.decoder.JSONDecodeError or TypeError as Error:
            print ("ERROR: ", self.levelPath, "is likely corrupt! JSON failed")
        
        try:
            JSONCHECKER(self.level,True) #make sure Jason is still good coming in
        except Exception as e:
            print (str(e) + " in "+ self.levelPath)
            raise
            
        return True

    def nextLevel(self):
        '''Attempts to load the next level, if success returns True, else False'''
        self.levelNumber += 1
        # self.levelName
        # self.levelPath = "levels/"+"level"+str(self.levelNumber)+".json"
        self.success = self.__levelLoad__()
        return self.success


    
    def getEvents(self, levelTime): 
        '''Will fetch all the events for the current time from
        level dictionary'''
        try:
            events = self.level["time"][str(levelTime)]
        except:
            return False #GUI handles false with no behavior
        timeEvents = {"player":[],"enemy":[],"bullets":[],"items":[]}
        del self.level["time"][str(levelTime)] #removes this time entry from the dictionary
        

        for each in events:
            if each in TIME_TYPES:
                if each == "player":
                    playerShip = player.player(events[each]["weapon"],events[each]["image"],events[each]["scheme"])
                    timeEvents["player"].append(playerShip)
                if each == "enemy":
                    health = events[each]["health"]
                    for enemyType in events[each]["class"]:
                        enemy = self.enemyClass(enemyType, health)
                        timeEvents["enemy"].append(enemy)
                if each == "enemyBullets":
                    for bulletType in events[each]["class"]:
                        bullet = self.bulletClass(bulletType)
                        timeEvents["bullets"].append(bullet)
                if each == "items":
                    for items in events[each]["class"]:
                        # item = self.bulletClass(bulletType)
                        # timeEvents["items"].append(item)
                        pass
                if each == "background":
                    timeEvents["background"]=events[each]
            else:
                print (each, " is not in levelLibrary TIME_TYPES so it will not be loaded")

        
        return timeEvents #all sprites and background in a dictionary returned to GUI

        # bad_guy = enemy.enemy('spitfire','enemy.png')


    def getEndBehavior(self):
        '''returns how the level can end'''
        try:
            events = self.level["end"]
        except:
            return False #GUI handles false with no behavior
        
        return events #returns dictionary with "time" last time in level and boss at end "true or false"
        

    def enemyClass(self,className, health):
        '''contructs and returns enemies based off a 1 input nameing convention'''
        ''' can add enemy classes, just contruct new enemy type'''
        enemySprite = None
        if className[0]=="@": #quick naming scheme ex: "@s1-d-3-1" -check levelLibrary.py for more
            a=className[1::].split("-")
            if PROPER_FORMAT(className):
                if len(a)==4:
                    enemySprite = enemy.enemy(ENEMY_SECTORS(a[0]), behavior=ENEMY_TYPE_MAP(a[1]), speed=int(a[2]), health=int(a[3]))
                else:     
                    enemySprite = enemy.enemy(ENEMY_SECTORS(a[0]), behavior=ENEMY_TYPE_MAP(a[1]), speed=int(a[2]), health=int(a[3]), acceleration=float(a[4]))
                return enemySprite
        

        if className == ENEMY_diveLeft:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s2"), health=health) # this will change, need to add spawn location and behavior
        elif className == ENEMY_diveRight:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s12")) # this will change, need to add spawn location and behavior
        elif className == ENEMY_diveMid1:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s5"), behavior="diver", health=health)
        elif className == ENEMY_diveMid2:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s7"), behavior="diver", health=health)
        elif className == ENEMY_diveMid3:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s9"), behavior="diver",health=health)
        
        
        elif className == ENEMY_sleeperMid:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s6"), behavior="sleeper",health=health)
        
        elif className == ENEMY_camperMid:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s7"), behavior="camper",health=health)
        elif className == ENEMY_camperRight:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s13"), behavior="camper",health=health)
        elif className == ENEMY_weakCamperMid:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s8"), behavior="camper",health=health) #gets no health scaler
        
        
        
        elif className == ENEMY_crazyMid1:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s4"), behavior="crazy",health=health)
        elif className == ENEMY_crazyMid2:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s6"), behavior="crazy",health=health)
        elif className == ENEMY_crazyMid3:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s8"), behavior="crazy",health=health)
            
        elif className == ENEMY_crazy2Mid1:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s2"), behavior="crazyReverse",health=health, speed=2)
        elif className == ENEMY_crazy2Mid2:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s13"), behavior="crazyReverse",health=health, speed=6)
        elif className == ENEMY_crazy2Mid3:
            enemySprite = enemy.enemy(ENEMY_SECTORS("s7"), behavior="crazyReverse",health=health, speed=9) #gets no health scaler
        
        
        else:#middle diver is fallback
            enemySprite = enemy.enemy(ENEMY_SECTORS("s7"), health=health) # this will change, need to add spawn location and behavior
        
        return enemySprite


        
    def playerClass(self,className):
        '''contructs and returns player object for spawn purposes, 
            could load a player saved state profile for unique ships'''
        pass
    
    def bulletClass (self,className):
        '''contructs and returns enemy bullets off a 1 input nameing convention'''
        bulletSprite = None
        if className == "downwardLeft":
            bulletSprite = bullet.bullet(COLUMN_WIDTH*1,0, -5, "bullet_art.png", 180 )# this will change, need to add spawn location and behavior
        elif className == "downwardRight":
            bulletSprite = bullet.bullet(COLUMN_WIDTH*4,0, 5, "bullet_art.png", 180 ) # this will change, need to add spawn location and behavior
        else:#middle bullet is fallback
            bulletSprite = bullet.bullet(SCREEN_WIDTH//2,0, 5, "bullet_art.png", 180 )# this will change, need to add spawn location and behavior
        return bulletSprite

        #delete items for each time called
        
#
#************* automated tests run below
#
if __name__ == "__main__":
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    pygame.display.set_caption('Testy mcTetsterson')

    dic ={}
    loader = LevelLoader() #loads level 1 by default
    pretendLevelTime=0
    
    while loader.success:
        levelEndTime = loader.getEndBehavior()["time"] #needs error checkingi n case level doesn't have end time. Also levels could hae end boss as well
        
        dic=loader.getEvents(pretendLevelTime) #dic returns False if nothing to load at that time
        if dic != False:
            print(loader.levelName)
            print("TIME: " , pretendLevelTime, " " , dic)

        pretendLevelTime +=1
        if pretendLevelTime == levelEndTime:
            loader.nextLevel()
            pretendLevelTime =0


    
    # print ("HERE IT IS",dic)
    
        