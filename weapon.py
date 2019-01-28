'''
File: weapon.py
01/28/19
'''


#each weapon name will be mapped to its function, an image, and other properties
def spitfire():
    print('spitfire here')

master_weapons_dict = {
    'spitfire': (spitfire, "dot.png", 15)

}


class Weapon(object):

    def __init__(self, weaponName):
        self.name = weaponName
        self.weapon_func = master_weapons_dict.get(weaponName)[0]
        #self.damage = master_weapons_dict.get(weaponName)[2]
        #print(damage)
        print(master_weapons_dict.get('spitfire')[0])


testWeapon = Weapon('spitfire')
testWeapon.weapon_func()