
#!/bin/python
#this file will load files made by level loader, and retrun all the values in the format expected by the GUI,
#To not have to change the GUI's functionality to much, levelLoader is kind of like a helper class for GUI

import weapon
import player
import enemy


import json




class LevelLoader():
    def __init__(self, startingLevelNumber):
        self.levelNumber = startingLevelNumber
        self.levelName = "levels/"+"level"+str(self.levelNumber)+".json"
        self.level = None
        self.__levelLoad__()
        self.DICTYPES = ["time", "end"]
        self.TIME_TYPES = ["player", "enemy", "enemyBullets", "background"]
        self.PLAYER_TYPES = ["health", "location", "image"]
        self.ENEMY_TYPES = ["class", "health"]
        self.ENEMYBULLETS_TYPE = ["class"]


    def __levelLoad__(self):
        with open (self.levelName,"r") as read_file:
            self.level= json.load(read_file)

    def nextLevel(self):
        self.levelNumber += 1
        self.levelName = "level"+self.levelNumber 
        self.level = self.__levelLoad__()


    
    def getEvents(self, levelTime): 
        '''Will fetch all the events for the current time from
        level dictionary'''
        try:
            events = self.level["time"][str(levelTime)]
        except:
            return False #GUI handles false with no behavior
        sprites = []

        for each in events:
            if each in self.TIME_TYPES:
                if each == "player":
                    print(events[each])
                    playerShip = player.player(events[each]["weapon"],events[each]["image"],events[each]["scheme"])
                    # print(playerShip)
        # bad_guy = enemy.enemy('spitfire','enemy.png')


    def getEndBehavior(self):
        '''returns how the level can end'''
        pass
        
        

    def enemyClass(self,className):
        '''contructs and returns enemies based off a 1 input nameing convention'''
        pass
        
    def playerClass(self,className):
        '''contructs and returns player object for spawn purposes'''
        pass
    
    def bulletClass (self,className):
        '''contructs and returns enemy bullets off a 1 input nameing convention'''
        pass

        #delete items for each time called
        
#
#************* automated tests run below
#
if __name__ == "__main__":
    loader = LevelLoader(3)
    loader.getEvents(0)

        