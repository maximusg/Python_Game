#filename: unitTestMain
#purpose: centralized script that runs all unit tests in a test suite

import unittest

import TestEntity
import TestHighscore
import TestLibrary
import TestAssetLoader
import TestGUI
import TestWeapon
import TestLevelLoader
import TestExplosionAnims

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestEntity.TestEntity))
    test_suite.addTest(unittest.makeSuite(TestHighscore.TestEntry))
    test_suite.addTest(unittest.makeSuite(TestHighscore.TestScoreboard))
    test_suite.addTest(unittest.makeSuite(TestLibrary.TestLibrary))
    test_suite.addTest(unittest.makeSuite(TestAssetLoader.TestAssetLoader))
    test_suite.addTest(unittest.makeSuite(TestGUI.TestGUI))
    test_suite.addTest(unittest.makeSuite(TestWeapon.TestWeapon))
    test_suite.addTest(unittest.makeSuite(TestLevelLoader.TestLevelLoader))
    test_suite.addTest(unittest.makeSuite(TestExplosionAnims.TestAnims))
    #add the rest of the unittests above this line

    return test_suite




mySuite=suite()


runner=unittest.TextTestRunner()
runner.run(mySuite)
