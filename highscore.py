#!/bin/python

import pathlib

def sanitizeName(value):
    if len(value) > 60:
        return value[:60]
    return value

def checkNumerical(value):
    if value == None or not isinstance(value, int):
        raise RuntimeError(value + 'is not a valid input.')
    return value

class scoreboard(object):

    class score_entry(object):
        def __init__(self, name, score):
            self.score = score
            self.name = name
            self.nextEntry = None
            self.prevEntry = None
        
        @property
        def score(self):
            return self.__score

        @property
        def name(self):
            return self.__name

        @property
        def nextEntry(self):
            return self.__nextEntry

        @score.setter
        def score(self, value):
            self.__score = checkNumerical(value)
        
        @name.setter
        def name(self, value):
            self.__name = sanitizeInput(value)
        
        @nextEntry.setter
        def nextEntry(self, value):
            if not None or not isinstance(value, self.__class__):
                raise RuntimeErorr(value + 'is not a valid scoreboard entry')
            self.__nextEntry = value

    def __init__(self):
        self.head = None
        self.tail = None
        pass
    
    def add(self, value):
        if not isinstance(value, self.score_entry):
            raise RuntimeError(value + 'is not a valid scoreboard entry')
        if not self.head:
            self.head = value
            self.tail = value
        else:
            while currEntry.score > value.score and currEntry.nextEntry != None:
                currEntry = currEntry.nextEntry
            value.prevEntry = currEntry.prevEntry
            value.nextEntry = currEntry
            value.prevEntry.nextEntry = value
            currEntry.prevEntry = value

    def getOnList(self, value):
        if value <= self.tail.value:
            return False
        return True

    def reset(self):
        self.head = None
        self.tail = None

    def __str__(self):
        currEntry = self.head
        result = ''
        result += '***HALL OF FAME!!!***\n'
        if currEntry != None:
            while currEntry.nextEntry:
                result += currEntry.name + ',' + str(currEntry.score)
        return result
        
if __name__ == '__main__':
    high_score_list = scoreboard()
    print(high_score_list)