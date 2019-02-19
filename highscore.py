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

        def __str__(self):
            return self.name + '  |  ' + str(self.score)
        
    def __init__(self):
        self.head = None
        self.tail = None
        self.readFromFile('resources/event_scrolls/highscores.asset')

    @property
    def head(self):
        return self.__head

    @property
    def tail(self):
        return self.__tail

    @head.setter
    def head(self, value):
        if not isinstance(value, Scoreboard.Entry) and value != None:
            raise RuntimeError(value + 'is not a valid head entry.')
        self.__head = value

    @tail.setter
    def tail(self, value):
        if not isinstance(value, Scoreboard.Entry) and value != None:
            raise RuntimeError(value + 'is not a valid head entry.')
        self.__tail = value

    def add(self, name, score):
        entry = self.Entry(name, score)
        if self.head == None:
            self.head = entry
            self.tail = entry

        if self.head.score < entry.score:
            entry.nextEntry = self.head
            self.head = entry
        else:
            currEntry = self.head
            while currEntry.nextEntry != None and currEntry.nextEntry.score >= entry.score:
                currEntry = currEntry.nextEntry
            entry.nextEntry = currEntry.nextEntry
            currEntry.nextEntry = entry
        self.__trim()

    def resetList(self):
        self.head = None
        self.tail = None

    def belongsOnList(self, score):
        return score > self.tail.score

    def writeToFile(self, filename):
        fileName = open(filename, 'w')
        currEntry = self.head
        while currEntry.nextEntry:
            if currEntry.nextEntry.nextEntry != None:
                fileName.write(currEntry.name+'.'+str(currEntry.score)+',')
            else:
                fileName.write(currEntry.name+'.'+str(currEntry.score))
            currEntry = currEntry.nextEntry
        fileName.close()

    def readFromFile(self, fileName):
        with open(fileName) as f:
            read_data = f.read().split(',')
        for entry in read_data:
            temp = entry.split('.')
            self.add(temp[0],int(temp[1]))


    def __trim(self):
        currEntry = self.head
        i = 0
        while currEntry.nextEntry != None and i < 21:
            currEntry = currEntry.nextEntry
            i += 1
        self.tail = currEntry
        self.tail.nextEntry = None 

    def __str__(self):
        result = '***HALL OF FAME!***\n'
        currEntry = self.head
        i = 1
        #result += str(i) + ') ' + str(currEntry) + '\n'
        #i += 1
        while currEntry.nextEntry:
            result += str(i) + ') ' + str(currEntry) + '\n'
            i += 1
            currEntry = currEntry.nextEntry
        result += str(i) + ') ' + str(currEntry) + '\n'
        return result


    
