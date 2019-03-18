'''Contains all the dependent shared code between levelMaker.py and levelLoader.py JSON checker tool and enemy 
spawn dictionaries dictionary, as well as an enemy simple contruct language to uniquely create enemy entities dynamically'''

from itemDropTables import *
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
        "db": "diveBomb",
        "ds": "diveStrafe"
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
        if len(b) >=5: #if acceleration added
                try:
                    int(b[4])
                except:
                    try:
                        float(b[4])
                    except:
                        return False
        if len(b) ==5: return True #no drop table item
        if len(b) ==6: #check for drop table items
                if b[5] in DTDic:
                    return True
                else:
                    print("item not in DTDic", a)
    return False


''' use'-' between @ENEMY_TYPE_MAP - ENEMY_SECTORS - speed - health - **acceleration**'''
def cluster (selection="full",b="db",s=3,h=1,d="DTcommon"):
    '''Use this function in levelMaker to create clusters of enemy, b=behavior must be in levelMaker dictionary
    s=speed, 
    h=health. 
    Selections to choose from are:
    "full"- creates enemies with atributes in all sectors
    "L3-L5"- creates left most 3 4 or 5 enenmies
    "R3-R5"- creates right most 3 5 or 5 enemies
    "M3-M5" - middle sectors 3 4 or 5 enemies
    "ML3-ML5" - middle Left sectors 3 4 or 5 enemies
    "MR3-MR5" - middle Right sectors 3 4 or 5 enemies
    '''
    h = str(h)
    s = str(s)
    basic = ["@s1-"+b+"-"+s+"-"+h+"-0-"+d, "@s2-"+b+"-"+s+"-"+h+"-0-"+d, "@s3-"+b+"-"+s+"-"+h+"-0-"+d, "@s4-"+b+"-"+s+"-"+h+"-0-"+d, "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d, "@s9-"+b+"-"+s+"-"+h+"-0-"+d, "@s10-"+b+"-"+s+"-"+h+"-0-"+d, "@s11-"+b+"-"+s+"-"+h+"-0-"+d, "@s12-"+b+"-"+s+"-"+h+"-0-"+d, "@s13-"+b+"-"+s+"-"+h+"-0-"+d, "@s14-"+b+"-"+s+"-"+h+"-0-"+d]
    return { 
        "full": basic, 
        "L3": ["@s1-"+b+"-"+s+"-"+h+"-0-"+d, "@s2-"+b+"-"+s+"-"+h+"-0-"+d, "@s3-"+b+"-"+s+"-"+h+"-0-"+d],
        "L4": ["@s1-"+b+"-"+s+"-"+h+"-0-"+d, "@s2-"+b+"-"+s+"-"+h+"-0-"+d, "@s3-"+b+"-"+s+"-"+h+"-0-"+d, "@s4-"+b+"-"+s+"-"+h+"-0-"+d],
        "L5": ["@s1-"+b+"-"+s+"-"+h+"-0-"+d, "@s2-"+b+"-"+s+"-"+h+"-0-"+d, "@s3-"+b+"-"+s+"-"+h+"-0-"+d, "@s4-"+b+"-"+s+"-"+h+"-0-"+d, "@s5-"+b+"-"+s+"-"+h+"-0-"+d],
        
        "R3": ["@s14-"+b+"-"+s+"-"+h+"-0-"+d, "@s13-"+b+"-"+s+"-"+h+"-0-"+d, "@s12-"+b+"-"+s+"-"+h+"-0-"+d],
        "R4": ["@s14-"+b+"-"+s+"-"+h+"-0-"+d, "@s13-"+b+"-"+s+"-"+h+"-0-"+d, "@s12-"+b+"-"+s+"-"+h+"-0-"+d, "@s11-"+b+"-"+s+"-"+h+"-0-"+d],
        "R5": ["@s14-"+b+"-"+s+"-"+h+"-0-"+d, "@s13-"+b+"-"+s+"-"+h+"-0-"+d, "@s12-"+b+"-"+s+"-"+h+"-0-"+d, "@s11-"+b+"-"+s+"-"+h+"-0-"+d, "@s10-"+b+"-"+s+"-"+h+"-0-"+d],
        
        "M3": [ "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d],
        "M4": [ "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d],
        "M5": [ "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d, "@s9-"+b+"-"+s+"-"+h+"-0-"+d],

       
        "ML3": ["@s4-"+b+"-"+s+"-"+h+"-0-"+d, "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d],
        "ML4": ["@s4-"+b+"-"+s+"-"+h+"-0-"+d, "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d],
        "ML5": ["@s4-"+b+"-"+s+"-"+h+"-0-"+d, "@s5-"+b+"-"+s+"-"+h+"-0-"+d, "@s6-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d],
        
        
        "MR3": ["@s11-"+b+"-"+s+"-"+h+"-0-"+d, "@s10-"+b+"-"+s+"-"+h+"-0-"+d, "@s9-"+b+"-"+s+"-"+h+"-0-"+d],
        "MR4": ["@s11-"+b+"-"+s+"-"+h+"-0-"+d, "@s10-"+b+"-"+s+"-"+h+"-0-"+d, "@s9-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d],
        "MR5": ["@s11-"+b+"-"+s+"-"+h+"-0-"+d, "@s10-"+b+"-"+s+"-"+h+"-0-"+d, "@s9-"+b+"-"+s+"-"+h+"-0-"+d, "@s8-"+b+"-"+s+"-"+h+"-0-"+d, "@s7-"+b+"-"+s+"-"+h+"-0-"+d],
        
       
    }.get(selection,basic) # defaults to basic
    
    
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

