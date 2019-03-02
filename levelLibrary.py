#Enemy simple contruct scheme

''' use'-' between @ENEMY_TYPE_MAP - ENEMY_SECTORS - speed - health - **acceleration**'''
''' updated: added acceleration as an optional'''
#example
'''@s1-d-3-1-0'''#uses @ sign to signal it is a simple contruct
#sector and type, looked up in maps below

#name map
def ENEMY_TYPE_MAP(x):
    return{
        "d":"diver",
        "c": "camper",
        "s": "sleeper",
        "cz": "crazy",
        "cr": "crazyReverse",
        "mv": "mrVectors",
        "db": "diveBomb"
    }.get(x,"diver") #defaults to diver

#enemy top screen sectors
def ENEMY_SECTORS (x):
    return { 
        "s1": [400,0], 
        "s2": [480,0],
        "s3": [560,0],
        "s4": [640,0],
        "s5": [720,0],
        "s6": [800,0],
        "s7": [880,0],
        "s8": [960,0],
        "s9": [1040,0],
        "s10": [1120,0],
        "s11": [1200,0],
        "s12": [1280,0],
        "s13": [1360,0],
        "s14": [1440,0],
    }.get(x,[880,0]) # defaults to s7

def PROPER_FORMAT(a):
    '''checks enemy simple constructis properly formated'''
    if a[0]== "@":
        b = a[1::].split("-")
        if len(b) >=4: #no acceleration
            try:
                int(b[2])
            except:
                return False
            try:
                int(b[3])
            except:
                return False
        if len(b) == 4: return True #no acceleration
        if len(b) ==5: #if acceleration added
                try:
                    int(b[4])
                except:
                    try:
                        float(b[4])
                    except:
                        return False

                return True
    return False


''' use'-' between @ENEMY_TYPE_MAP - ENEMY_SECTORS - speed - health - **acceleration**'''
def fullDiveCluster (selection="basic"):
    basic = ["@s1-db-0-1-.01", "@s2-db-0-1-.01", "@s3-db-0-1-.01", "@s4-db-0-1-.01", "@s5-db-0-1-.01", "@s6-db-0-1-.01", "@s7-db-0-1-.01", "@s8-db-0-1-.01", "@s9-db-0-1-.01", "@s10-db-0-1-.01", "@s11-db-0-1-.01", "@s12-db-0-1-.01", "@s13-db-0-1-.01", "@s14-db-0-1-.01"]
    return { 
        "basic": basic, 
        "lvl1": ["@s1-db-0-1-.03", "@s2-db-0-1-.03", "@s3-db-0-1-.03", "@s4-db-0-1-.03", "@s5-db-0-1-.03", "@s6-db-0-1-.03", "@s7-db-0-1-.03", "@s8-db-0-1-.03", "@s9-db-0-1-.03", "@s10-db-0-1-.03", "@s11-db-0-1-.03", "@s12-db-0-1-.03", "@s13-db-0-1-.03", "@s14-db-0-1-.03"],
        "lvl2": ["@s1-db-0-1-.04", "@s2-db-0-1-.04", "@s3-db-0-1-.04", "@s4-db-0-1-.04", "@s5-db-0-1-.04", "@s6-db-0-1-.04", "@s7-db-0-1-.04", "@s8-db-0-1-.04", "@s9-db-0-1-.04", "@s10-db-0-1-.04", "@s11-db-0-1-.04", "@s12-db-0-1-.04", "@s13-db-0-1-.04", "@s14-db-0-1-.04"],
        "lvl3": ["@s1-db-0-1-.05", "@s2-db-0-1-.05", "@s3-db-0-1-.05", "@s4-db-0-1-.05", "@s5-db-0-1-.05", "@s6-db-0-1-.05", "@s7-db-0-1-.05", "@s8-db-0-1-.05", "@s9-db-0-1-.05", "@s10-db-0-1-.05", "@s11-db-0-1-.05", "@s12-db-0-1-.05", "@s13-db-0-1-.05", "@s14-db-0-1-.05"],
        "lvl4": ["@s1-db-0-1-.06", "@s2-db-0-1-.06", "@s3-db-0-1-.06", "@s4-db-0-1-.06", "@s5-db-0-1-.06", "@s6-db-0-1-.06", "@s7-db-0-1-.06", "@s8-db-0-1-.06", "@s9-db-0-1-.06", "@s10-db-0-1-.06", "@s11-db-0-1-.06", "@s12-db-0-1-.06", "@s13-db-0-1-.06", "@s14-db-0-1-.06"],
        "lvl5": ["@s1-db-0-1-.07", "@s2-db-0-1-.07", "@s3-db-0-1-.07", "@s4-db-0-1-.07", "@s5-db-0-1-.07", "@s6-db-0-1-.07", "@s7-db-0-1-.07", "@s8-db-0-1-.07", "@s9-db-0-1-.07", "@s10-db-0-1-.07", "@s11-db-0-1-.07", "@s12-db-0-1-.07", "@s13-db-0-1-.07", "@s14-db-0-1-.07"],
        "lvl6": ["@s1-db-0-1-.08", "@s2-db-0-1-.08", "@s3-db-0-1-.08", "@s4-db-0-1-.08", "@s5-db-0-1-.08", "@s6-db-0-1-.08", "@s7-db-0-1-.08", "@s8-db-0-1-.08", "@s9-db-0-1-.08", "@s10-db-0-1-.08", "@s11-db-0-1-.08", "@s12-db-0-1-.08", "@s13-db-0-1-.08", "@s14-db-0-1-.08"],
        "lvl7": ["@s1-db-0-1-.09", "@s2-db-0-1-.09", "@s3-db-0-1-.09", "@s4-db-0-1-.09", "@s5-db-0-1-.09", "@s6-db-0-1-.09", "@s7-db-0-1-.09", "@s8-db-0-1-.09", "@s9-db-0-1-.09", "@s10-db-0-1-.09", "@s11-db-0-1-.09", "@s12-db-0-1-.09", "@s13-db-0-1-.09", "@s14-db-0-1-.09"],
        "lvl8": ["@s1-db-0-1-.1", "@s2-db-0-1-.1", "@s3-db-0-1-.1", "@s4-db-0-1-.1", "@s5-db-0-1-.1", "@s6-db-0-1-.1", "@s7-db-0-1-.1", "@s8-db-0-1-.1", "@s9-db-0-1-.1", "@s10-db-0-1-.1", "@s11-db-0-1-.1", "@s12-db-0-1-.1", "@s13-db-0-1-.1", "@s14-db-0-1-.1"],
        "lvl9": ["@s1-db-0-1-.11", "@s2-db-0-1-.11", "@s3-db-0-1-.11", "@s4-db-0-1-.11", "@s5-db-0-1-.11", "@s6-db-0-1-.11", "@s7-db-0-1-.11", "@s8-db-0-1-.11", "@s9-db-0-1-.11", "@s10-db-0-1-.11", "@s11-db-0-1-.11", "@s12-db-0-1-.11", "@s13-db-0-1-.11", "@s14-db-0-1-.11"],
        "lvl10": ["@s1-db-0-3-.03", "@s2-db-0-3-.03", "@s3-db-0-3-.03", "@s4-db-0-3-.03", "@s5-db-0-3-.03", "@s6-db-0-3-.03", "@s7-db-0-3-.03", "@s8-db-0-3-.03", "@s9-db-0-3-.03", "@s10-db-0-3-.03", "@s11-db-0-3-.03", "@s12-db-0-3-.03", "@s13-db-0-3-.03", "@s14-db-0-3-.03"],
        "lvl11": ["@s1-db-0-6-.03", "@s2-db-0-6-.03", "@s3-db-0-6-.03", "@s4-db-0-6-.03", "@s5-db-0-6-.03", "@s6-db-0-6-.03", "@s7-db-0-6-.03", "@s8-db-0-6-.03", "@s9-db-0-6-.03", "@s10-db-0-6-.03", "@s11-db-0-6-.03", "@s12-db-0-6-.03", "@s13-db-0-6-.03", "@s14-db-0-6-.03"],
        "lvl12": ["@s1-db-0-9-.03", "@s2-db-0-9-.03", "@s3-db-0-9-.03", "@s4-db-0-9-.03", "@s5-db-0-9-.03", "@s6-db-0-9-.03", "@s7-db-0-9-.03", "@s8-db-0-9-.03", "@s9-db-0-9-.03", "@s10-db-0-9-.03", "@s11-db-0-9-.03", "@s12-db-0-9-.03", "@s13-db-0-9-.03", "@s14-db-0-9-.03"],
        "lvl13": ["@s1-db-0-9-.06", "@s2-db-0-9-.06", "@s3-db-0-9-.06", "@s4-db-0-9-.06", "@s5-db-0-9-.06", "@s6-db-0-9-.06", "@s7-db-0-9-.06", "@s8-db-0-9-.06", "@s9-db-0-9-.06", "@s10-db-0-9-.06", "@s11-db-0-9-.06", "@s12-db-0-9-.06", "@s13-db-0-9-.06", "@s14-db-0-9-.06"],
        "lvl14": ["@s1-db-0-11-.06", "@s2-db-0-11-.06", "@s3-db-0-11-.06", "@s4-db-0-11-.06", "@s5-db-0-11-.06", "@s6-db-0-11-.06", "@s7-db-0-11-.06", "@s8-db-0-11-.06", "@s9-db-0-11-.06", "@s10-db-0-11-.06", "@s11-db-0-11-.06", "@s12-db-0-11-.06", "@s13-db-0-11-.06", "@s14-db-0-11-.06"],
        "lvl15": ["@s1-db-2-20-.03", "@s2-db-2-20-.03", "@s3-db-2-20-.03", "@s4-db-2-20-.03", "@s5-db-2-20-.03", "@s6-db-2-20-.03", "@s7-db-2-20-.03", "@s8-db-2-20-.03", "@s9-db-2-20-.03", "@s10-db-2-20-.03", "@s11-db-2-20-.03", "@s12-db-2-20-.03", "@s13-db-2-20-.03", "@s14-db-2-20-.03"],
        "lvl16": ["@s1-db-8-20-.03", "@s2-db-8-20-.03", "@s3-db-8-20-.03", "@s4-db-8-20-.03", "@s5-db-8-20-.03", "@s6-db-8-20-.03", "@s7-db-8-20-.03", "@s8-db-8-20-.03", "@s9-db-8-20-.03", "@s10-db-8-20-.03", "@s11-db-8-20-.03", "@s12-db-8-20-.03", "@s13-db-8-20-.03", "@s14-db-8-20-.03"],
        "lvl17": ["@s1-db-10-20-.03", "@s2-db-10-20-.03", "@s3-db-10-20-.03", "@s4-db-10-20-.03", "@s5-db-10-20-.03", "@s6-db-10-20-.03", "@s7-db-10-20-.03", "@s8-db-10-20-.03", "@s9-db-10-20-.03", "@s10-db-10-20-.03", "@s11-db-10-20-.03", "@s12-db-10-20-.03", "@s13-db-10-20-.03", "@s14-db-10-20-.03"],

        # "s4": [720,0],
        # "s5": [800,0],
        # "s6": [880,0],
        # "s7": [960,0],
        # "s8": [1040,0],
        # "s9": [1120,0],
        # "s10": [1200,0],
        # "s11": [1280,0],
        # "s12": [1360,0],
        # "s13": [1440,0],
        # "s14": [1520,0],
    }.get(selection,basic) # defaults to s7
    
    
    

















#Enemy Classes
ENEMY_diveLeft ="diveLeft"
ENEMY_diveRight ="diveRight"
ENEMY_diveMid1 = "diveMid1"
ENEMY_diveMid2 = "diveMid2"
ENEMY_diveMid3 = "diveMid3"


ENEMY_sleeperMid ="sleeperMid"

ENEMY_weakCamperMid = "weakCamperMid"
ENEMY_camperMid ="camperMid"
ENEMY_camperRight ="camperRight"


ENEMY_crazyMid1 = "crazyMid1"
ENEMY_crazyMid2 = "crazyMid2"
ENEMY_crazyMid3 = "crazyMid3"

ENEMY_crazy2Mid1 = "crazy2Mid1"
ENEMY_crazy2Mid2 = "crazy2Mid2"
ENEMY_crazy2Mid3 = "crazy2Mid3"

ENEMY_basicCluster = [ENEMY_diveLeft,ENEMY_diveRight, ENEMY_camperMid, ENEMY_camperRight, ENEMY_sleeperMid]


ENEMY_diveCluster = [ENEMY_diveLeft,ENEMY_diveRight, ENEMY_diveMid1, ENEMY_diveMid2]

ENEMY_crazyCluster = [ENEMY_crazyMid1,ENEMY_crazyMid2,ENEMY_crazyMid3,ENEMY_crazy2Mid1,ENEMY_crazy2Mid2,ENEMY_crazy2Mid3]

#Bullet Classes
BULLET_downwardLeft = "downwardLeft"
BULLET_downwardRight = "downwardRight"

#Backgrounds
BG_STARFIELD = "starfield.png"


#verifying  Properly formatted
TIME_TYPES = ["player", "enemy", "enemyBullets", "background", "items", "boss_sprite"]
END_TYPES =["boss","time"]


DICTYPES = {
    "time":{ 0:{ #int check
         "player":{
            "health":1, #inttype
            "image":"stringType",
            "location":[2], #array size 2 w/ inttypes
            "scheme":"stringType",
            "weapon":"stringType"
        },
        "enemy":{
            "class":["strings"], #array type w/ stringtypes
            "health": 1 #int type
        },
        "boss_sprite": {
            "image":"stringType",
            "class":["strings"]           
        },
        "enemyBullets":{
            "class":["strings"] #array type w/ stringtypes
        },
        "background":"stringType"
    } #REQ
       
    }, 
    "end":{ #REQ
        "boss":False, #boolean
        "time": 10 #integerType
    
    }
}


def JSONCHECKER(pythonDICT,JSON):
    #high level check
    for item in pythonDICT:
        if item not in DICTYPES:
            raise TypeError ("\'"+item + "\' is not allowed")
        
    #intermediate level
    timeCheck = pythonDICT["time"]#starts a layer up from timeDict, as it needs to check at each time
    timeDICT = DICTYPES["time"][0] #get types, makes calls shorter
    for timek in timeCheck:
        time = timek
        if JSON:
            if  isinstance( time, int) : #when it comes back from JSON it is a string but I'm overlooking this check for ease of conversions
                raise TypeError( str(time) + ' is incorrect time type') 
        else:
            if  isinstance (timek, str):
                time = int(timek) #converts back to int, will throw exception on its own if not a number

        
        for check in timeCheck[time]:
            if check not in timeDICT: #checks "player enemy bullet  and background" are the only things here
                raise TypeError (str(check) +" is not allowed")
            
            #low level looking inside each object
            for req in timeDICT[check]:
                if check != "background":
                    if req not in timeCheck[time][check]: #checks for inside player, enemy, bullet, background enforces each required
                        raise RuntimeError (req +" missing in " + check + " at time "+  str(time))
                    if not isinstance(timeCheck[time][check][req], type(timeDICT[check][req])): #checks types are what are to be expected inside each
                        raise TypeError (str(check) +" has wrong type for "+req+" at time " + str(time))
            
            if check == "background": #since background is not an object it needs special treatments
                if not isinstance(timeCheck[time][check], type(timeDICT[check])): #checks types are what are to be expected inside each
                        raise TypeError (str(check) +" has wrong type at time " + str(time))                
    
    timeCheck = pythonDICT["end"]
    timeDICT = DICTYPES["end"]
   
    for item in timeCheck:
        if item not in timeDICT:
            raise TypeError ("end item \'" + item + "\' is not allowed")

        if not isinstance(timeCheck[item], type(timeDICT[item])):
            raise TypeError ("end item \'" + item + "\' should be " + str(type(timeDICT[item])) )


    return "Good"




            #     if  not isinstance(location, Point.Point) :
            # raise RuntimeError(location + ' is not a Point') 

