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
                "class": [ ENEMY_camperMid ],
                "health": 1
                },
            "enemyBullets":{
                "class": [ BULLET_downwardLeft,BULLET_downwardRight ],
                },
            "background": BG_STARFIELD

            },
            5: #time 5 seconds elapsed
            {"enemy":{
                "class":[ ENEMY_diveLeft,ENEMY_diveRight] ,
                "health": 1
                },
            },
            10: #time 5 seconds elapsed
            {"enemy":{
                "class":ENEMY_basicCluster,
                "health": 1
                },
            }
    },
    "end": {"time":15, "boss":False} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

if JSONCHECKER(data,False) == "good":

    #When we execute levelMaker in Python, it saves a copy of the script we build
    with open (writeLocation,"w") as write_file:
        json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
