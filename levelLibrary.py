#Enemy Classes
ENEMY_diveLeft ="diveLeft"
ENEMY_diveRight ="diveRight"
ENEMY_sleeperMid ="sleeperMid"
ENEMY_camperMid ="camperMid"
ENEMY_camperRight ="camperRight"
ENEMY_weakCamperMid = "weakCamperMid"

ENEMY_basicCluster = [ENEMY_diveLeft,ENEMY_diveRight, ENEMY_camperMid, ENEMY_camperRight, ENEMY_sleeperMid]

#Bullet Classes
BULLET_downwardLeft = "downwardLeft"
BULLET_downwardRight = "downwardRight"

#Backgrounds
BG_STARFIELD = "starfield.png"


#verifying  Properly formatted
TIME_TYPES = ["player", "enemy", "enemyBullets", "background", "items"]
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

