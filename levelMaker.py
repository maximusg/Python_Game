import json
from library import *


##Create Levels here with this level maker! Just make a dictionary with spawn times and enemies, and the background elements.
#then run the script, make sure to not overwrite a file unintentially.




levelName="level3.json" #level follwed level_number
writeLocation = "levels/"+levelName
data = {
    "time":{ 0: #time zero
            {"player":{ #starting info if dead
                "health":1,
                "location":(500,700),
                "image":"SweetShip.png"
                },
            "enemy":{
                "number":2,
                "weapons":["spitfire","spitfire"],
                "images":["enemy.png","enemy.png"],
                "behaviors": ["dive","spin"],
                "health": 1, #enemyhealth= enemyClassHealth*1
                "centers":[(0,0),(50,0)]
                },
            "enemyBullets":{
                "number":1,
                "images":["bullet_art.png"],
                "behaviors": ["horizontal_spitfire"],
                "centers":[(900,400)]
                }
            },
            5: #time 5 seconds elapsed
            {"enemy":{ #note that player info removed
                "number":3,
                "weapons":["spitfire","spitfire","spitefire"],
                "images":["enemy.png","enemy.png", "enemy.png"],
                "behaviors": ["dive","spin","dive"],
                "layer":[BG,GROUND,ITEM,AIR,OVERHEAD],
                "health": 2, #enemyhealth= enemyClassHealth*2
                "centers":[(0,0),(300,0),(800,0)]
                },
            "enemyBullets":{# note, there are zero bullets thus other properties uncessary
                "number":0,
                "images":[],
                "behaviors": [],
                "centers":[]
                }
            }
        },
        "end": {"time":15, "boss":None} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

#When we execute levelMaker in Python, it saves a copy of the script we build
with open (writeLocation,"w") as write_file:
    json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
