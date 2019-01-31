class Scoreboard(object):
    class Entry(object):
        def __init__(self, name, score):
            self.name = name
            self.score = score
            self.nextEntry = None
        
        @property
        def name(self):
            return self.__name

        @property
        def score(self):
            return self.__score

        @property
        def nextEntry(self):
            return self.__nextEntry

        @name.setter
        def name(self, nameIn):
            if not isinstance(nameIn, str):
                raise RuntimeError(nameIn + 'is not a valid name for score entry')
            self.__name = nameIn
        
        @score.setter
        def score(self, scoreIn):
            if not isinstance(scoreIn, int):
                raise RuntimeError(scoreIn + 'is not a valid score for score entry')
            self.__score = scoreIn

        @nextEntry.setter
        def nextEntry(self, entryIn):
            if not (isinstance(entryIn, self.__class__) or entryIn == None):
                raise RuntimeError(entryIn + 'is not a valid assignment for nextEntry')
            self.__nextEntry = entryIn
        
    def __init__(self):
        self.head = None
        self.tail = None
        self.__length = 0

    def add(self, entry):
        currEntry = self.head
        while currEntry.score > entry.score:
            pass

    def resetList(self):
        self.head = None
        self.tail = None
        self.__length = 0

    def belongsOnList(self, score):
        return score > self.tail.score

    def writeToFile(self):
        pass

    def readFromFile(self):
        pass
        
