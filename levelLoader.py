
#!/bin/python
#this file will load files made by level loader, and retrun all the values in the format expected by the GUI,
#To not have to change the GUI's functionality to much, levelLoader is kind of like a helper class for GUI
import Entity

import weapon
from library import *
from levelLibrary import *
import json
from itemDropTables import *






class LevelLoader():
    '''API to get level information for all the events starting at level1.json by default from the level folder.
        Can get ending or current loaded level, and all the of the sprites will get contructed and sent in a dictionary
        at the requested time, which can then be loaded into the GUI'''
    
    def __init__(self, startingLevelNumber=1):
        self.levelNumber = startingLevelNumber
        self.level = None
        self.success = self.__levelLoad__()
       
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
    
        

    def __levelLoad__(self):
        '''level loader function, will use a path to load in the next level JSON and get all the events in a dictionary
            Also checks that JSON file is still vailid with JSONCHECKER'''
        
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
        timeEvents = {"player":[],"enemy":[],"bullets":[],"items":[],"boss_sprite":[]}
        del self.level["time"][str(levelTime)] #removes this time entry from the dictionary
        

        for each in events:
            if each in TIME_TYPES:
                if each == "player":
                    playerShip = Entity.Player(init_wep=events[each]["weapon"],imgFile=events[each]["image"],scheme=events[each]["scheme"])
                    timeEvents["player"].append(playerShip)
                if each == "enemy":
                    for enemyType in events[each]["class"]:
                        enemy = self.enemyClass(enemyType)
                        timeEvents["enemy"].append(enemy)
                if each == 'boss_sprite':
                    image = events[each]["image"]
                    boss = self.bossClass(image)
                    timeEvents["boss_sprite"].append(boss)
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
                    timeEvents["background"]=BACKGROUND_PATH.joinpath(events[each])
            else:
                print (each, " is not in levelLibrary TIME_TYPES so it will not be loaded")

        
        return timeEvents #all sprites and background in a dictionary returned to GUI

        # bad_guy = Entity.Enemy('spitfire','enemy.png')


    def getEndBehavior(self):
        '''returns how the level can end'''
        try:
            events = self.level["end"]
        except:
            return False #GUI handles false with no behavior
        
        return events #returns dictionary with "time" last time in level and boss at end "true or false"
        

    def enemyClass(self,className):
        '''contructs and returns enemies based off a 1 input nameing convention'''
        ''' can add enemy classes, just contruct new enemy type'''
        enemySprite = None
        if className[0]=="@": #quick naming scheme ex: "@s1-d-3-1" -check levelLibrary.py for more
            a=className[1::].split("-")
            
            if PROPER_FORMAT(className):
                
                if len(a)==4:
                    enemySprite = Entity.Enemy(ENEMY_SECTORS(a[0]), behavior=ENEMY_TYPE_MAP(a[1]), speed=int(a[2]), health=int(a[3]))
                elif len(a)==5:     
                    enemySprite = Entity.Enemy(ENEMY_SECTORS(a[0]), behavior=ENEMY_TYPE_MAP(a[1]), speed=int(a[2]), health=int(a[3]), acceleration=float(a[4]))
                else: #length is 6
                    item = DTDic[a[5]]
                    
                    enemySprite = Entity.Enemy(ENEMY_SECTORS(a[0]), behavior=ENEMY_TYPE_MAP(a[1]), speed=int(a[2]), health=int(a[3]), acceleration=float(a[4]), itemDropTable=item)
                return enemySprite
        

        if className == ENEMY_diveLeft:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s2")) # this will change, need to add spawn location and behavior
        elif className == ENEMY_diveRight:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s12")) # this will change, need to add spawn location and behavior
        elif className == ENEMY_diveMid1:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s5"), behavior="diver")
        elif className == ENEMY_diveMid2:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s7"), behavior="diver")
        elif className == ENEMY_diveMid3:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s9"), behavior="diver")
        
        
        elif className == ENEMY_sleeperMid:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s6"), behavior="sleeper")
        
        elif className == ENEMY_camperMid:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s7"), behavior="camper")
        elif className == ENEMY_camperRight:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s13"), behavior="camper")
        elif className == ENEMY_weakCamperMid:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s8"), behavior="camper") #gets no health scaler
        
        
        
        elif className == ENEMY_crazyMid1:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s4"), behavior="crazy")
        elif className == ENEMY_crazyMid2:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s6"), behavior="crazy")
        elif className == ENEMY_crazyMid3:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s8"), behavior="crazy")
            
        elif className == ENEMY_crazy2Mid1:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s2"), behavior="crazyReverse", speed=2)
        elif className == ENEMY_crazy2Mid2:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s13"), behavior="crazyReverse", speed=6)
        elif className == ENEMY_crazy2Mid3:
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s7"), behavior="crazyReverse", speed=9) #gets no health scaler
        
        
        else:#middle diver is fallback
            enemySprite = Entity.Enemy(ENEMY_SECTORS("s7")) # this will change, need to add spawn location and behavior
        
        return enemySprite

    def bossClass(self, image):
        return Entity.BossSprite(ENEMY_SECTORS("s7"), image)

    
    def bulletClass (self,className):
        '''contructs and returns enemy bullets off a 1 input nameing convention'''
        bulletSprite = None
        if className == "downwardLeft":
            bulletSprite = Entity.Bullet(COLUMN_WIDTH*1,0, -5, "bullet_art.png", 180 )# this will change, need to add spawn location and behavior
        elif className == "downwardRight":
            bulletSprite = Entity.Bullet(COLUMN_WIDTH*4,0, 5, "bullet_art.png", 180 ) # this will change, need to add spawn location and behavior
        else:#middle bullet is fallback
            bulletSprite = Entity.Bullet(SCREEN_WIDTH//2,0, 5, "bullet_art.png", 180 )# this will change, need to add spawn location and behavior
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
    
        