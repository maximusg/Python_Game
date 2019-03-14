#filename: unitTestMain
#purpose: centralized script that runs all unit tests in a test suite

import unittest

import TestEntity
import TestHighscore
import TestLibrary

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestEntity.TestEntity))
    #add the rest of the unittests below this line

    return test_suite




mySuite=suite()


runner=unittest.TextTestRunner()
runner.run(mySuite)
