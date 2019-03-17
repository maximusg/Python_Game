import unittest
import movement
import Entity

class TestMovement(unittest.TestCase):
    
    def test__init__(self):
        pass
        goodmoveCountArray1 = [1,2]
        goodmoveCountArray2 = [0]
        goodmoveCountArray3 = [0,1,2,3,4,5,6,7,8,9,10]

        badmoveCountArray1 = "a"
        badmoveCountArray2 = ["a"]
        badmoveCountArray3 = 11
        badmoveCountArray4 = [1.2]
        badmoveCountArray5 = [0,1.2]


        goodVectorArray1 =[["x","x","x"]]
        goodVectorArray2 =[["x","x",0]]
        goodVectorArray3 =[["x","x",100]]
        goodVectorArray4 =[["x","x",100.1]]
        goodVectorArray5 =[["x",0,"x"]]
        goodVectorArray6 =[["x",100,"x"]]
        goodVectorArray7 =[["x",100.1,"x"]]
        goodVectorArray8 =[[0,"x","x"]]
        goodVectorArray9 =[[100,"x","x"]]
        goodVectorArray10 =[[100.1,"x","x"]]
        goodVectorArray11 =[[0,0,0]]
        goodVectorArray12 =[[.1,.1,.1]]
        goodVectorArray13 =[[0,-1,0]]
        goodVectorArray14 =[[0,0,-1]]
        goodVectorArray15 =[[-1,0,0]]
        goodVectorArray16 =[[0,0,0],[0,"x",1]]
        goodVectorArray17 =[[0,0,0],[0,"x",1],["x","x","x"]]

        badVectorArray1 = [0,0,0]
        badVectorArray2 = [["a",0,0]]
        badVectorArray2 = [[0,"a",0]]
        badVectorArray2 = [[0,0,"a"]]
        badVectorArray2 = [[0,0,0],["a",0,0]]
        badVectorArray3 = [[0,0,0],"A"]
        badVectorArray4 = [[0,0,0],1]
        badVectorArray5 = [[0,0,0],["x",0,[1]]]
        badVectorArray6 = [0,0,[]]

        goodrepeat1 = 0
        goodrepeat2 = 1
        goodrepeat3 = 10000

        badrepeat1 =[1]
        badrepeat2 = "a"
        badrepeat3 = -1

        ####valid tests###
        flag = False
        try:
            movement.Move(moveCountArray=goodmoveCountArray1)
            movement.Move(moveCountArray=goodmoveCountArray2)
            movement.Move(moveCountArray=goodmoveCountArray3)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=goodVectorArray1)
            movement.Move(vectorAray=goodVectorArray2)
            movement.Move(vectorAray=goodVectorArray3)
            movement.Move(vectorAray=goodVectorArray4)
            movement.Move(vectorAray=goodVectorArray5)
            movement.Move(vectorAray=goodVectorArray6)
            movement.Move(vectorAray=goodVectorArray7)
            movement.Move(vectorAray=goodVectorArray8)
            movement.Move(vectorAray=goodVectorArray9)
            movement.Move(vectorAray=goodVectorArray10)
            movement.Move(vectorAray=goodVectorArray11)
            movement.Move(vectorAray=goodVectorArray12)
            movement.Move(vectorAray=goodVectorArray13)
            movement.Move(vectorAray=goodVectorArray14)
            movement.Move(vectorAray=goodVectorArray15)
            movement.Move(vectorAray=goodVectorArray16)
            movement.Move(vectorAray=goodVectorArray17)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
        
        flag = False
        try:
            movement.Move(repeat=goodrepeat1)
            movement.Move(repeat=goodrepeat2)
            movement.Move(repeat=goodrepeat3)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
        
        ####invalid tests###
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray1)
            movement.Move(moveCountArray=badmoveCountArray2)
            movement.Move(moveCountArray=badmoveCountArray3)
            movement.Move(moveCountArray=badmoveCountArray4)
            movement.Move(moveCountArray=badmoveCountArray5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray1)
            movement.Move(vectorAray=badVectorArray2)
            movement.Move(vectorAray=badVectorArray3)
            movement.Move(vectorAray=badVectorArray4)
            movement.Move(vectorAray=badVectorArray5)
            movement.Move(vectorAray=badVectorArray6)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(repeat=badrepeat1)
            movement.Move(repeat=badrepeat2)
            movement.Move(repeat=badrepeat3)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

if __name__ == "__main__":
    unittest.main(exit=False)