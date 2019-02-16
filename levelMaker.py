import json
from library import *


##Create Levels here with this level maker! Just make a dictionary with spawn times and enemies, and the background elements.
#then run the script, make sure to not overwrite a file unintentially.




levelName="level2.json" #level follwed level_number
writeLocation = "levels/"+levelName
data = {
    "time":{ 0: #time zero
            {"player":{ #starting info if dead
                "health":1,
                "location":(500,700),
                "image":"SweetShip.png",
                "weapon": "spitfire",
                "scheme": " arrows",
                },
            "enemy":{
                "class":["diveLeft","diveRight"],
                "health": 1
                },
            "enemyBullets":{
                "class": ["downwardLeft","downwardRight"],
                },
            "background": "starfield.png"

            },
            5: #time 5 seconds elapsed
            {"enemy":{
                "class":["camperMid","camperRight"],
                "health": 1
                },
            },
            10: #time 5 seconds elapsed
            {"enemy":{
                "class":["diverLeft","camperRight"],
                "health": 1
                },
            }
        },
    "end": {"time":15, "boss":False} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

#When we execute levelMaker in Python, it saves a copy of the script we build
with open (writeLocation,"w") as write_file:
    json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
