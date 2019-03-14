#filename: TestEntity.py
#purpose: Unit tests for the Entity class


import unittest

import Entity

class TestEntity(unittest.TestCase):

    def test__init__(self):
        #first, let's verify that the attributes are what we'd expect from the constructor
        origin = (1, 5)
        #imageFile = str(Path(UNIT_TESTS_PATH).joinpath('test.png'))
        acceleration = 666
        speed = 65
        angle = 109
        health = 44
        point_value = 314

        e = Entity.Entity(origin=origin,  acceleration= acceleration, speed= speed, angle=angle, health= health, point_value= point_value)
        self.assertEqual(e.rect.x, origin[0])
        self.assertEqual(e.rect.y, origin[1])
        
        self.assertEqual(e.acceleration, acceleration)
        self.assertEqual(e.speed, speed)
        self.assertEqual(e.health, health)
        self.assertEqual(e.value, point_value)


        #let's test different types of valid Entities, the flag should stay False
        flag = False
        try:
            e1 = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=0, health= 15, point_value= 22)
            e2 = Entity.Entity(origin=(1,65),  acceleration= 2, speed= 41, angle=10, health= 150, point_value= 220)
            e3 = Entity.Entity(origin=(10,51),  acceleration= 5, speed= 14, angle=4, health= 155, point_value= 15)
            e4 = Entity.Entity(origin=(31,5),  acceleration= 250, speed= 94, angle=7, health= 88, point_value= 88)

        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)

        #break health, health must be int
        bad_val = 'healthy'
        flag = False
        try:
            e1 = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=0, health= bad_val, point_value= 22)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


        #break acceleration, must be int or float
        bad_val = 'vrooom'
        flag = False
        try:
            e1 = Entity.Entity(origin=(1,5),  acceleration= bad_val, speed= 4, angle=0, health= 4, point_value= 22)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        #break angle, must be int or float
        bad_val = None
        flag = False
        try:
            e1 = Entity.Entity(origin=(1,5),  acceleration= 56, speed= 4, angle=bad_val, health= 4, point_value= 22)
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)

        #break speed, must be int or float
        bad_val = 'zoom'
        flag = False
        try:
            e1 = Entity.Entity(origin=(1,5),  acceleration= 56, speed= bad_val, angle=0, health= 4, point_value= 22)
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)


    def testSetHealth(self):
        bad_health_string = 'so healthy'
        bad_health_float = 4.2
        health_test_val = 5
        e = Entity.Entity(health = health_test_val)
        self.assertEqual(e.health, health_test_val)
        new_good_health = 2
        e.health = new_good_health
        self.assertEqual(e.health, new_good_health)

        #health can't be a string
        flag = False
        try:
            e.health = bad_health_string
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        #health can't be None
        flag = False
        try:
            e.health = None
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)

        #health can't be a float
        flag = False
        try:
            e.health = 4.2
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)

        #good health
        flag = False
        try:
            e.health = 10
            e.health = 10000
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)


    def testSetRotation(self):
        bad_rotation_string = 'so rotaty'
        bad_rotation_float = 4.2
        rotation_test_val = 5
        e = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=0, health= 15, point_value= 22)

        #rotation setter value can't be a string
        flag = False
        try:
            e.rotation = bad_rotation_string
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        #rotation setter value can't be a float
        flag = False
        try:
            e.rotation = bad_rotation_float
        except TypeError as te:
            flag = True
        finally:
            self.assertTrue(flag)

        #good rotation set
        flag = False
        try:
            e.rotation = rotation_test_val
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
    
    def testSetSpeed(self):
        bad_speed_string = 'much speed'
        good_speed_float = 4.2
        good_speed_int = 5
        e = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=0, health= 15, point_value= 22)

        #speed setter value can't be a string
        flag = False
        try:
            e.speed = bad_speed_string
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        #speed setter value can't be a float
        flag = False
        try:
            e.speed = good_speed_float
        except TypeError as te:
            flag = True
        finally:
            self.assertFalse(flag)

        #good speed set
        flag = False
        try:
            e.speed = good_speed_int
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
        
    def testSetAcceleration(self):
        bad_acceleration_string = 'much acceleration'
        good_acceleration_float = 4.2
        good_acceleration_int = 5
        e = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=0, health= 15, point_value= 22)

        #acceleration setter value can't be a string
        flag = False
        try:
            e.acceleration = bad_acceleration_string
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        #acceleration setter value can't be a float
        flag = False
        try:
            e.acceleration = good_acceleration_float
        except TypeError as te:
            flag = True
        finally:
            self.assertFalse(flag)

        #good acceleration set
        flag = False
        try:
            e.acceleration = good_acceleration_int
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)

    def testUpdateSpeed(self):
        e = Entity.Entity(origin=(1,5),  acceleration= 25, speed= 4, angle=45, health= 15, point_value= 22)
        e.updateSpeed()
        expected_speedY = str(e.speedY)[:10]
        expected_speedX = str(e.speedX)[:10]
        self.assertEqual(expected_speedX, '20.5060966')
        self.assertEqual(expected_speedY, '20.5060966')

    #not working for some reason...
    # def testMove(self):
    #     e = Entity.Entity(origin=(20,20),  acceleration= 25, speed= 4, angle=45, health= 15, point_value= 22)
    #     print(e.rect.x, e.rect.y)
    #     e.move(1,1)
    #     print(e.rect.x, e.rect.y)

#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)

