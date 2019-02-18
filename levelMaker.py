import json
# from library import *
from levelLibrary import *


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
                "class": [ENEMY_crazyMid1, ENEMY_diveLeft],
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
    "end": {"time":37, "boss":False} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

print(JSONCHECKER(data,False))

#When we execute levelMaker in Python, it saves a copy of the script we build
with open (writeLocation,"w") as write_file:
    json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
