import unittest
import pygame
import levelLoader
import os


class TestLevelLoader(unittest.TestCase):
    
    def test__init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        loader=levelLoader.LevelLoader(0)
        events = loader.level
        e=loader.getEvents(0)
        self.assertEqual(os.path.basename(e['player'][0].imageFile),"SweetShip.png")
        self.assertEqual(os.path.basename(e['background']),"starfield.png")
        self.assertEqual(e['player'][0].rect.x, 920)#these come from library
        self.assertEqual(e['player'][0].rect.y, 860)
        self.assertEqual(e['player'][0].control_scheme, "arrows")
        self.assertEqual(e['player'][0].weapon.name, 'blue_lazer')

    def test__getEvent__(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        loader=levelLoader.LevelLoader(0)
       
        self.assertFalse(loader.getEvents("not a valid time"))
        sprite = loader.getEvents(3)
        self.assertFalse(loader.getEvents(3))#should erase from loader
       
       #make sure proper enemy is created
        speed=sprite["enemy"][0].speed
        acceleration=sprite["enemy"][0].acceleration
        angle=sprite["enemy"][0].angle
        health=sprite["enemy"][0].health
        itemDropTable=sprite["enemy"][0].itemDropTable
       
        self.assertEqual(speed,3)
        self.assertEqual(acceleration,0)
        self.assertEqual(angle,0)
        self.assertEqual(health,1)
        self.assertEqual(itemDropTable,('spitfire_powerup',1))

    def test_getEndBehavior(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        loader=levelLoader.LevelLoader(0)
        e=loader.getEndBehavior()
 

        self.assertTrue(e["boss"])
        self.assertEqual(e['time'],80)

    def test_nextLevel(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        loader=levelLoader.LevelLoader(0)
        level0 = loader.level
        self.assertTrue(loader.nextLevel())
        level1 = loader.level
        self.assertFalse(level0 == level1)



        


if __name__ == "__main__":
    unittest.main(exit=False)