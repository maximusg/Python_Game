import unittest
import movement
import Entity
import pygame

class TestMovement(unittest.TestCase):
    
    def test__init__(self):
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
        goodrepeat4 = -1

        badrepeat1 =[1]
        badrepeat2 = "a"
        

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
            movement.Move(repeat=goodrepeat4)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertFalse(flag)
        
        ####invalid tests###
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray1)
        except RuntimeError as rte:
            flag = True
        finally:
                self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray2)
        except RuntimeError as rte:
                flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray3)
        except RuntimeError as rte:
                flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray4)
        except RuntimeError as rte:
                flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(moveCountArray=badmoveCountArray5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray1)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False  
        try:
            movement.Move(vectorAray=badVectorArray2)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray3)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray4)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray5)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(vectorAray=badVectorArray6)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            movement.Move(repeat=badrepeat1)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            movement.Move(repeat=badrepeat2)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def test__updateCurrMove__(self):
        moveCountArray = [2,0]
        vectorArray = [[1,3,0]]
        repeat = 1
        move = movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=repeat)
        move.__updateCurrMove__()
        self.assertTrue(move.currMove == 2)
        self.assertTrue(move.currVector == [1,3,0])
        self.assertTrue(move.moveCounts == [0])
        self.assertTrue(move.repeat == 1)
        move.__updateCurrMove__()
        self.assertTrue(move.currMove == 1)
        self.assertTrue(move.currVector == [1,3,0])
        self.assertTrue(move.moveCounts == [0])
        self.assertTrue(move.repeat == 1)
        move.__updateCurrMove__()
        self.assertTrue(move.currMove == 0)
        self.assertTrue(move.currVector == [1,3,0])
        self.assertTrue(move.moveCounts == [0])
        self.assertTrue(move.repeat == 1)
        move.__updateCurrMove__()
        self.assertTrue(move.currMove == 0) #updates to next ne MoveCounts
        self.assertTrue(move.currVector == [1,3,0])
        self.assertTrue(move.moveCounts == []) #pops from moveCounts and places in currMove
        self.assertTrue(move.repeat == 1)
        
        self.assertTrue(move.__updateCurrMove__(),False) #returns false when no more moveCounts and currMove==0
    
    def testUpdate(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        screen.fill((0,0,0))
        pygame.display.set_caption('Testy mcTetsterson')
        enemy = Entity.Enemy(origin=(500,0),speed=0, acceleration=0, angle=0)
        
        
        moveCountArray = [1]
        vectorArray = [[1,"x","x"]]
        repeat = 1
        #accelerate enemy at 1 pixel/update,  down  at (angle =0)
        move = movement.Move(moveCountArray=moveCountArray, vectorAray=vectorArray,repeat=repeat)
       
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 0.0)
        self.assertEqual(move.repeat, 1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 0)
        move.update(enemy)
        
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 1.0)
        self.assertEqual(move.repeat, 1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 1)
        move.update(enemy)
     
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 2.0)
        self.assertEqual(move.repeat, 1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 3)
        move.update(enemy) #reloads w/ repeat =1
       
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 3.0)
        self.assertEqual(move.repeat, 0)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 6)
        move.update(enemy)
       
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 4.0)
        self.assertEqual(move.repeat, 0)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 10)
       
       
        move.update(enemy)#loads in off screen behavior continues 801 moves after second load.
        #loads in  moveCounts=[1,800] and vectors=[[2,0,0],["x","x","x"]]
        self.assertTrue(move.moveCounts==[800])
        self.assertTrue(move.vectors==[["x","x","x"]]) 
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 2.0)
        self.assertEqual(move.repeat, -1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 12)
        move.update(enemy)
        
        self.assertTrue(move.moveCounts==[800])
        self.assertTrue(move.vectors==[["x","x","x"]]) 
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 2.0)
        self.assertEqual(move.repeat, -1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 14)
        move.update(enemy)
        
        self.assertTrue(move.moveCounts==[])
        self.assertTrue(move.vectors==[])
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 4.0)
        self.assertEqual(move.repeat, -1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 18)
        move.update(enemy)
        
        self.assertTrue(move.moveCounts==[])
        self.assertTrue(move.vectors==[])
        self.assertEqual(enemy.speedX, 0.0) 
        self.assertEqual(enemy.speedY, 6.0)
        self.assertEqual(move.repeat, -1)
        self.assertEqual(enemy.rect.x, 500)
        self.assertEqual(enemy.rect.y, 24)

        #... contintuees to move enemy accelerating off screen downward.
       
       
       
       
       
       
       
       
        # self.assertEqual(enemy.speedY, 5.0)
        
        
       
        # self.assertEqual(enemy.speedY, 4.0)





if __name__ == "__main__":
    unittest.main(exit=False)