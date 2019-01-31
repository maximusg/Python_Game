class Weapon():
    def __init__(weaponName=None):
        self.name = weaponName
        behaviourDic={"spitfire":(spitfire(),4,"imgs/dot.png")}

    #behaviours
    def spitfire(self,dmg,file):
        howManySpawnAtOnce = 3 #always a number.
        numberOfGuns=2
        howFast=2
        direction1=[(-1,1*howFast),(1,1*howFast),(-1,1*howFast)]
        directionOfDirections=[direction1,direction2]

        return (howManySpawnAtOnce,howFast,directionOfDirections,file,dmg)
    
    
    


