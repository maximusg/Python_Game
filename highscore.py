#CONSTANTS
MAX_ENTRIES = 20 #Change this to grow or shrink the high score list

class Scoreboard(object):
    '''Linked List data structure that contains the High Score List for Day0.'''

    class Entry(object):
        '''Object representing a single entry within the overall Scoreboard class. Contains:
            name - Must be a string.
            score - Must be an integer.
            nextEntry - Must point to the next Entry object in the list (can be None).
        '''
        def __init__(self, name, score):
            '''Initializes Entry with string name and int score.'''

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
                raise RuntimeError(str(nameIn) + ' is not a valid name for score entry')
            self.__name = nameIn
        
        @score.setter
        def score(self, scoreIn):
            if not isinstance(scoreIn, int):
                raise RuntimeError(str(scoreIn) + ' is not a valid score for score entry')
            self.__score = scoreIn

        @nextEntry.setter
        def nextEntry(self, entryIn):
            if not (isinstance(entryIn, self.__class__) or entryIn == None):
                raise RuntimeError(entryIn + ' is not a valid assignment for nextEntry')
            self.__nextEntry = entryIn

        def __str__(self):
            return self.name + '  |  ' + str(self.score)
        
    def __init__(self):
        '''Initializes the high score list and loads in the persistent list from disk.'''

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
            raise RuntimeError(str(value) + 'is not a valid head entry.')
        self.__head = value

    @tail.setter
    def tail(self, value):
        if not isinstance(value, Scoreboard.Entry) and value != None:
            raise RuntimeError(str(value) + 'is not a valid tail entry.')
        self.__tail = value

    def add(self, name, score):
        '''Adds an entry into the linked list sorted based on score. Assumes it "belongs" on the list already.'''
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
        '''Resets the list by removing all contents, then readding dummy values to refill.
           Does __NOT__ write out the new list to disk, you must do that manually.'''
        self.head = None
        self.tail = None
        for i in range(MAX_ENTRIES):
            self.add('CRN', 10000)

    def belongsOnList(self, score):
        '''Returns true if the score is higher than the lowest score on the list. Requires a fully populated list.'''
        return score > self.tail.score

    def writeToFile(self, filename):
        '''Write the list out to file based on a simple delimiter scheme. Periods deliniate the name from the score,
           while commas deliniate between entries.'''
        fileName = open(filename, 'w')
        currEntry = self.head
        while currEntry:
            if currEntry.nextEntry != None:
                fileName.write(currEntry.name+'.'+str(currEntry.score)+',')
            else:
                fileName.write(currEntry.name+'.'+str(currEntry.score))
            currEntry = currEntry.nextEntry
        fileName.close()

    def readFromFile(self, fileName):
        '''Reads in a file, breaks it down based on periods separating name and score and commas separating entries, and 
           automatically readds each entry into the list.'''
        with open(fileName) as f:
            read_data = f.read().split(',')
        for entry in read_data:
            temp = entry.split('.')
            self.add(temp[0],int(temp[1]))


    def __trim(self):
        '''Trims the list to length set by MAX_ENTRIES. Should not be called directly.''' 
        currEntry = self.head
        i = 1
        while currEntry.nextEntry != None and i < MAX_ENTRIES:
            currEntry = currEntry.nextEntry
            i += 1
        self.tail = currEntry
        self.tail.nextEntry = None 

    def __str__(self):
        result = '***HALL OF FAME!***\n'
        currEntry = self.head
        i = 1
        while currEntry.nextEntry:
            result += str(i) + ') ' + str(currEntry) + '\n'
            i += 1
            currEntry = currEntry.nextEntry
        result += str(i) + ') ' + str(currEntry) + '\n'
        return result


    
