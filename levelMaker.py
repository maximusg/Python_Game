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
                "weapon": "blue_lazer",
                "scheme": "arrows",
                },
            "enemy":{
                "class": ["@s7-mv-0-1-0"],
                "health": 1
                },
            "background": BG_STARFIELD
            },
    },
    "end": {"time":150, "boss":False} #this gives the ending parameters
        #if time=None, then boss=imageName of poss sprite, once defeated


}

# #RUSH generator
# for i in range(36,50):
#     s1 = str((i%4)+1)
#     s2 = str((i%4)+2)
#     s3 = str((i%6)+5)
#     s4 = str((i%4)+9)
#     s5 = str((i%4)+11)
#     spd1 = str(random.randint(1,(i%10+1)))
#     data["time"][i] = {"enemy":{"class":["@s"+s2+"-d-3-1", "@s"+s1+"-d-4-1", "@s6-c-"+spd1+"-1", "@s"+s2+"-d-4-1", "@s"+s1+"-d-3-1"],"health": 1},}

# #RUSH generator
# for i in range(51,60):
#     s1 = str((i%4)+1)
#     s2 = str((i%4)+2)
#     s3 = str((i%6)+5)
#     s4 = str((i%4)+9)
#     s5 = str((i%4)+11)
#     spd1 = str(random.randint(1,(i%10+1)))
#     data["time"][i] = {"enemy":{"class":["@s"+s2+"-cr-3-1", "@s"+s1+"-c-4-1", "@s6-d-"+spd1+"-1", "@s"+s2+"-cr-4-1", "@s"+s1+"-c-3-1"],"health": 1},}


# #RUSH generator
# for i in range(61,90):
#     s1 = str((i%4)+1)
#     s2 = str((i%4)+2)
#     s3 = str((i%6)+5)
#     s4 = str((i%4)+9)
#     s5 = str((i%4)+11)
    
#     spd1 = str(random.randint(1,(i%10+1)))
#     data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-3-2", "@s"+s5+"-d-4-3", "@s"+s4+"-s-"+spd1+"-5", "@s"+s2+"-c-4-3", "@s"+s3+"-cr-3-2"],"health": 1},}


# #RUSH generator
# for i in range(91,130,2):
#     s1 = str((i%4)+1)
#     s2 = str((i%4)+2)
#     s3 = str((i%6)+5)
#     s4 = str((i%4)+9)
#     s5 = str((i%4)+11)
    
#     spd1 = str(random.randint(1,(i%10+1)))
#     spd2 = str(random.randint(1,(i%10+1)))
#     spd3 = str(random.randint(1,(i%10+1)))
#     spd4 = str(random.randint(1,(i%10+1)))
#     data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-"+spd2+"-2", "@s"+s5+"-c-"+spd3+"-2", "@s"+s4+"-s-"+spd1+"-6", "@s"+s2+"-d-"+spd3+"-2", "@s"+s3+"-d-"+spd4+"-2"],"health": 1},}
#     data["time"][i+1] = {"enemy":{"class":["@s"+s1+"-s-"+spd2+"-2", "@s"+s5+"-d-"+spd3+"-2", "@s"+s4+"-d-"+spd1+"-6", "@s"+s2+"-cr-"+spd3+"-2", "@s"+s3+"-c-"+spd4+"-2"],"health": 1},}
# #RUSH generator
# for i in range(131,150,2):
#     sc1 = str((i%4)+1)
#     sc2 = str((i%4)+2)
#     sc3 = str((i%6)+5)
#     sc4 = str((i%4)+9)
#     sc5 = str((i%4)+11)

#     sectorLoc = [sc1,sc2,sc3,sc4,sc5]
#     s1=sectorLoc.pop(random.randint(1,4))
#     s2=sectorLoc.pop(random.randint(1,3))
#     s3=sectorLoc.pop(random.randint(1,2))
#     s4=sectorLoc.pop(random.randint(1,1))
#     s5=sectorLoc.pop()

    
#     spd1 = str(random.randint(3,(i%10+3)))
#     spd2 = str(random.randint(3,(i%10+3)))
#     spd3 = str(random.randint(3,(i%10+3)))
#     spd4 = str(random.randint(3,(i%10+3)))
#     data["time"][i] = {"enemy":{"class":["@s"+s1+"-d-"+spd2+"-2", "@s"+s5+"-c-"+spd3+"-2", "@s"+s4+"-s-"+spd1+"-100", "@s"+s2+"-cz-"+spd3+"-2", "@s"+s3+"-cr-"+spd4+"-2"],"health": 1},}
#     data["time"][i+1] = {"enemy":{"class":["@s"+s1+"-c-"+spd2+"-2", "@s"+s5+"-d-"+spd3+"-2", "@s"+s4+"-d-"+spd1+"-2", "@s"+s2+"-d-"+spd3+"-2", "@s"+s3+"-s-"+spd4+"-100"],"health": 1},}

print(JSONCHECKER(data,False))

#When we execute levelMaker in Python, it saves a copy of the script we build
with open (writeLocation,"w") as write_file:
    json.dump (data, write_file, indent=4, sort_keys=True )


print(data)
