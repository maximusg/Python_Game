import unittest

import weapon

class TestWeapon(unittest.TestCase):

    def test__init__(self):
        good_weapon = 'spitfire'
        w = weapon.Weapon(good_weapon)

        self.assertEqual(w.name, good_weapon)

        #let's test different types of valid weapons, the flag should stay False
        flag = False
        try:
            w1 = weapon.Weapon('spitfire')
            w2 = weapon.Weapon('spitfire2')
            w3 = weapon.Weapon('spitfire3')
            w4 = weapon.Weapon('blue_lazer')
            w5 = weapon.Weapon('master_lazer')
            w6 = weapon.Weapon('missle')
            w7 = weapon.Weapon('bomb')
            w8 = weapon.Weapon('waveBeam')
            w9 = weapon.Weapon('waveBeam2')
            w10 = weapon.Weapon('waveBeam3')
            w11 = weapon.Weapon('chargeShot')
            w12 = weapon.Weapon('chargeShot2')
            w13 = weapon.Weapon('chargeShot3')

        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)

        #let's try to construct invalid weapons
        flag = False
        try:
            bad_w1 = weapon.Weapon('peashooter')
            bad_w2 = weapon.Weapon(4)
            bad_w3 = weapon.Weapon(None)
            bad_w4 = weapon.Weapon('spitfire', 'chargeShot')

        except RuntimeError as rte:
            flag = True

        finally:
            self.assertTrue(flag)

    def testGetters(self):
        name = 'spitfire'
        w = weapon.Weapon(name)
        speed = w.getSpeed(name)

        expected = weapon.master_weapons_dict.get(name)[3]
        self.assertEqual(speed, expected)

        imagePath = w.getImagePath(name)
        expected = weapon.master_weapons_dict.get(name)[2]
        self.assertEqual(imagePath, expected)

        damage = w.getDamage(name)
        expected = weapon.master_weapons_dict.get(name)[0]
        self.assertEqual(damage, expected)

