import json


##Create Levels here with this level maker! Just make a dictionary with spawn times and enemies, and the background elements.
#then run the script, make sure to not overwrite a file unintentially.


levelName="level1.json"
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

# with open ("levels/lvl1.json","w") as write_file:
#     json.dump (data,write_file)

print (data)

with open ("lvl1.json","r") as read_file:
    script= json.load(read_file)

print (script)