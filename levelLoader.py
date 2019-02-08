#this file will load files made by level loader, and retrun all the values in the format expected by the GUI,
#To not have to change the GUI's functionality to much, levelLoader is kind of like a helper class for GUI

import json

class levelLoader():
    def __init__(self, startingLevelNumber):
        self.levelNumber = startingLevelNumber
        self.levelName = "level"+self.levelNumber 
        self.level = self.__levelLoad__()
        

    def __levelLoad__(self):
        
        with open (self.levelName,"r") as read_file:
            self.level= json.load(read_file)

    def nextLevel(self):
        self.levelNumber += 1
        self.levelName = "level"+self.levelNumber 
        self.level = self.__levelLoad__()


    
    def getEvents(self, gameTime): 
        '''Will fetch all the events for the current time from
        level dictionary'''
        events = self.level["time"][gameTime]
        player_sprites, player_bullet_sprites, enemy_sprites, enemy_bullet_sprites = events


        