import pygame
import AssetLoader
import library
import unittest

class TestAssetLoader(unittest.TestCase):
    def test__init__(self):
        x = AssetLoader.AssetLoader()
        self.assertIsInstance(x.assets, dict)
    
    def testAssetModify(self):
        x = AssetLoader.AssetLoader()
        flag = False
        try:
            x.assets = []
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testGetAsset(self):
        x = AssetLoader.AssetLoader()
        filename_good = 'SweetShip.png'
        filename_bad = 'thisfiledoesnotexist.png'

        ##file not found
        flag = False
        try:
            image, rect = x.getAsset(filename_bad)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        ##display not initialized
        flag = False
        try:
            image, rect = x.getAsset(str(library.MISC_SPRITES_PATH.joinpath(filename_good)))
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        ##verify __loadAsset works
        pygame.display.init()
        pygame.display.set_mode((1,1))
        flag = True
        try:
            image, rect = x.getAsset(str(library.MISC_SPRITES_PATH.joinpath(filename_good)))
        except RuntimeError as rte:
            flag = False
        finally:
            self.assertTrue(flag)
            self.assertIsInstance(image, pygame.surface.Surface)
            self.assertIsInstance(rect, pygame.rect.Rect)
        
        pygame.display.quit()

        ##verify it is able to pull from the dict the second time
        pygame.display.init()
        pygame.display.set_mode((1,1))
        flag = True
        try:
            image, rect = x.getAsset(str(library.MISC_SPRITES_PATH.joinpath(filename_good)))
        except RuntimeError as rte:
            flag = False
        finally:
            self.assertTrue(flag)
            self.assertIsInstance(image, pygame.surface.Surface)
            self.assertIsInstance(rect, pygame.rect.Rect)

        flag = True
        try:
            image, rect = x.getAsset(str(library.MISC_SPRITES_PATH.joinpath(filename_good)))
        except RuntimeError as rte:
            flag = False
        finally:
            self.assertTrue(flag)
            self.assertIsInstance(image, pygame.surface.Surface)
            self.assertIsInstance(rect, pygame.rect.Rect)
        
        pygame.display.quit()

    def test__loadAsset(self):
        '''Function is verified during testGetAsset()'''
        pass

if __name__ == "__main__":
    unittest.main(exit=False)
        