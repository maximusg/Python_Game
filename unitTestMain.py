#filename: unitTestMain
#purpose: centralized script that runs all unit tests in a test suite

import unittest

import TestEntity
import TestHighscore
import TestLibrary
import TestAssetLoader

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestEntity.TestEntity))
    test_suite.addTest(unittest.makeSuite(TestHighscore.TestEntry))
    test_suite.addTest(unittest.makeSuite(TestHighscore.TestScoreboard))
    test_suit.addTest(unittest.makeSuite(TestLibrary.TestLibrary))
    test_suit.addTest(unittest.makeSuite(TestAssetLoader.TestAssetLoader))
    #add the rest of the unittests below this line

    return test_suite




mySuite=suite()


runner=unittest.TextTestRunner()
runner.run(mySuite)
