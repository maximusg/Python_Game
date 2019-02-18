import json
# from library import *
from levelLibrary import *
import random


##Create Levels here with this level maker! Just make a dictionary with spawn times and enemies, and the background elements.
#then run the script, make sure to not overwrite a file unintentially.




levelName="level1.json" #level follwed level_number
writeLocation = "levels/"+levelName
data = {
    "time":{ 0: #time zero
            {"player":{ #starting info if dead
                "health":1,
                "location":[500,700],
                "image":"SweetShip.png",
                "weapon": "spitfire",
                "scheme": "arrows",
                },
            "enemy":{
                "class": ["@s3-d-3-1", "@s5-d-4-1", "@s6-c-4-1", "@s7-d-4-1", "@s9-d-3-1"],
                "health": 1
                },
            "background": BG_STARFIELD

            },
            5: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            8: #time 5 seconds elapsed
            {"enemy":{
                "class":[ENEMY_crazy2Mid1, ENEMY_crazyMid1] ,
                "health": 1
                },
            },
            12: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_crazyCluster,
                "health": 1
                },
            },
            20: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_crazyCluster,
                "health": 1
                },
            },
            21: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            23: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            28: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_crazyCluster,
                "health": 1
                },
            },
            29: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            30: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            31: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            32: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_crazyCluster,
                "health": 99
                },
            },
            33: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 1
                },
            },
            34: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 3
                },
            },
            35: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_diveCluster,
                "health": 2
                },
            },

    },
    "end": {"time":150, "boss":False} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

#RUSH generator
for i in range(36,50):
    s1 = str(i%13)
    s2 = str(i%14)
    spd1 = str(random.randint(1,(i%10+1)))
    data["time"][i] = {"enemy":{"class":["@s"+s2+"-d-3-1", "@s"+s1+"-d-4-1", "@s6-c-"+spd1+"-1", "@s"+s2+"-d-4-1", "@s"+s1+"-d-3-1"],"health": 1},}

#RUSH generator
for i in range(51,60):
    s1 = str(i%13)
    s2 = str(i%14)
    spd1 = str(random.randint(1,(i%10+1)))
    data["time"][i] = {"enemy":{"class":["@s"+s2+"-cr-3-1", "@s"+s1+"-c-4-1", "@s6-d-"+spd1+"-1", "@s"+s2+"-cr-4-1", "@s"+s1+"-c-3-1"],"health": 1},}


#RUSH generator
for i in range(61,90):
    s1 = str(i%2)
    s2 = str(i%5)
    s3 = str(i%8)
    s4 = str(i%11)
    s5 = str(i%14)
    
    spd1 = str(random.randint(1,(i%10+1)))
    data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-3-1", "@s"+s5+"-d-4-1", "@s"+s4+"-s-"+spd1+"-1", "@s"+s2+"-c-4-1", "@s"+s3+"-cr-3-1"],"health": 1},}


#RUSH generator
for i in range(91,130):
    s1 = str(i%2)
    s2 = str(i%5)
    s3 = str(i%8)
    s4 = str(i%11)
    s5 = str(i%14)
    
    spd1 = str(random.randint(1,(i%10+1)))
    spd2 = str(random.randint(1,(i%10+1)))
    spd3 = str(random.randint(1,(i%10+1)))
    spd4 = str(random.randint(1,(i%10+1)))
    data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-"+spd2+"-1", "@s"+s5+"-c-"+spd3+"-1", "@s"+s4+"-s-"+spd1+"-1", "@s"+s2+"-cz-"+spd3+"-1", "@s"+s3+"-cr-"+spd4+"-1"],"health": 1},}

#RUSH generator
for i in range(131,150):
    sc1 = str(i%2)
    sc2 = str(i%5)
    sc3 = str(i%8)
    sc4 = str(i%11)
    sc5 = str(i%14)

    sectorLoc = [sc1,sc2,sc3,sc4,sc5]
    s1=sectorLoc.pop(random.randint(0,4))
    s2=sectorLoc.pop(random.randint(0,3))
    s3=sectorLoc.pop(random.randint(0,2))
    s4=sectorLoc.pop(random.randint(0,1))
    s5=sectorLoc.pop()

    
    spd1 = str(random.randint(3,(i%10+3)))
    spd2 = str(random.randint(3,(i%10+3)))
    spd3 = str(random.randint(3,(i%10+3)))
    spd4 = str(random.randint(3,(i%10+3)))
    data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-"+spd2+"-2", "@s"+s5+"-c-"+spd3+"-2", "@s"+s4+"-s-"+spd1+"-2", "@s"+s2+"-cz-"+spd3+"-2", "@s"+s3+"-cr-"+spd4+"-2"],"health": 1},}


print(JSONCHECKER(data,False))

#When we execute levelMaker in Python, it saves a copy of the script we build
with open (writeLocation,"w") as write_file:
    json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
