import highscore
import unittest
import os

class TestScoreboard(unittest.TestCase):
    def test__init__(self):
        board = highscore.Scoreboard()

        expected_head = highscore.Scoreboard.Entry('GAN', 582250)
        expected_tail = highscore.Scoreboard.Entry('CRN',10000)

        self.assertEqual(str(board.head), str(expected_head))
        self.assertEqual(str(board.tail), str(expected_tail))

    def testHeadSetter(self):
        board = highscore.Scoreboard()
        flag = False
        try:
            board.head = 42
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        board.head = board.tail
        self.assertEqual(board.head, board.tail)

    def testTailSetter(self):
        board = highscore.Scoreboard()
        flag = False
        try:
            board.tail = 42
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        board.tail = board.head
        self.assertEqual(board.head, board.tail)

    def testAdd(self):
        expected = '***HALL OF FAME!***\n'
        expected += '1) chris  |  42\n'
        expected += '2) greg  |  41\n'
        expected += '3) max  |  1\n'

        board = highscore.Scoreboard()

        board.head = None
        board.tail = None

        board.add('greg', 41)
        board.add('max', 1)
        board.add('chris', 42)

        self.assertEqual(expected, str(board))


    def testResetList(self):
        expected = '***HALL OF FAME!***\n'
        for i in range(1,21):
            expected += str(i)+') CRN  |  10000\n'

        board = highscore.Scoreboard()
        self.assertNotEqual(expected, str(board))

        board.resetList()
        self.assertEqual(expected, str(board))

    def testBelongsOnList(self):
        board = highscore.Scoreboard()
        board.resetList()

        flag = board.belongsOnList(42)
        self.assertFalse(flag)
        flag = board.belongsOnList(1000000000)
        self.assertTrue(flag)


    def testWriteToFile(self):
        expected = '***HALL OF FAME!***\n'
        expected += '1) chris  |  3\n'
        expected += '2) chris  |  2\n'
        expected += '3) chris  |  1\n'

        board = highscore.Scoreboard()
        
        board.head = None
        board.tail = None

        for i in range(1,4):
            board.add('chris', i)
        board.writeToFile('unittest.asset')

        board.head = None
        board.tail = None


        board.readFromFile('unittest.asset')
        self.assertEqual(expected, str(board))

        os.remove('unittest.asset')


    def testReadFromFile(self):
        '''Tested concurrently with WriteToFile'''
        pass

    def test__trim(self):
        board = highscore.Scoreboard()

        board.head = None
        board.tail = None

        for i in range(25):
            board.add('chris', i)
        self.assertEqual(board.tail.score, 5)

    def test__str__(self):
        board = highscore.Scoreboard()

        board.head = None
        board.tail = None

        board.add('chris', 10000)
        board.add('chris', 10001)
        result = '***HALL OF FAME!***\n'
        result += '1) chris  |  10001\n'
        result += '2) chris  |  10000\n'
        self.assertEqual(result, str(board))

    
class TestEntry(unittest.TestCase):
    def test__init__(self):
        name = 'chris'
        score = 10000
        entry = highscore.Scoreboard.Entry(name, score)

        self.assertEqual(entry.name, name)
        self.assertEqual(entry.score, score)
        self.assertEqual(entry.nextEntry, None)

    def testNameSetter(self):
        entry = highscore.Scoreboard.Entry('chris', 10000)
        
        flag = False
        try:
            entry.name = 5
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testScoreSetter(self):
        entry = highscore.Scoreboard.Entry('chris', 10000)
        
        flag = False
        try:
            entry.score = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testNextEntrySetter(self):
        entry = highscore.Scoreboard.Entry('chris', 10000)

        flag = False
        try:
            entry.nextEntry = '42'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def test__str__(self):
        name = 'chris'
        score = 10000
        entry = highscore.Scoreboard.Entry(name, score)
        result = 'chris  |  10000'

        self.assertEqual(str(entry), result)

if __name__ == "__main__":
    unittest.main(exit=False)