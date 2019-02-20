import pygame
import block
from pygame.locals import *
from pygame.compat import geterror
import random

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (0,   255,   0)
GREEN = (0,   0,   255)

class GUI(object):
    def __init__(self):
        ##Initialize pygame, set up the screen.
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
    
        pygame.display.set_caption('TESTER')
        pygame.mouse.set_visible(False)
        self.clock= pygame.time.Clock()
        self.clock.tick(60)

         #Clock setup
        self.clock = pygame.time.Clock()

        #Create sprite groups
        # group = pygame.sprite.Group()

        #Create Dirty Sprite group
        # group = pygame.sprite.LayeredDirty()

        #only works with this group type
        group = pygame.sprite.LayeredUpdates()

        
        

        # initalize blocks ORDER MATTERS when added to group
        # whiteBlock = block.Block(WHITE,60,80) #LOWEST LAYER
        # redBlock = block.Block(RED,60,90)

        # blueBlock = block.Block(BLUE,60,80)
        # greenBlock = block.Block(GREEN,60,90) #Highest LAYER
        
        
        redBlock = block.Block(group,RED,60,90,1) #Lowest LAYER
        whiteBlock = block.Block(group,WHITE,60,80,2) 

        blueBlock = block.Block(group,BLUE,60,80,3)
        greenBlock = block.Block(group,GREEN,60,90,4) #Highest LAYER
        # redBlock = block.Block(RED,60,90,1) #Lowest LAYER
        # whiteBlock = block.Block(WHITE,60,80,2) 

        # blueBlock = block.Block(BLUE,60,80,3)
        # greenBlock = block.Block(GREEN,60,90,4) #Highest LAYER

        # group.add(redBlock,whiteBlock,blueBlock,greenBlock)

        # blockGrp1.add(whiteBlock,redBlock)
        whiteBlock.rect.x = 50
        whiteBlock.rect.y = 60

        redBlock.rect.x = 100
        redBlock.rect.y = 60


        # blockGrp1.add(greenBlock,blueBlock)
        blueBlock.rect.x = 50
        blueBlock.rect.y = 200

        greenBlock.rect.x = 100
        greenBlock.rect.y = 200
        
        blueBlock.dirty=2
        greenBlock.dirty=1

        # print(blueBlock.layer())
        self.screen.fill(BLACK)
        done=False
        pygame.display.flip()
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                whiteBlock.visible=0
                whiteBlock.rect.y += -1
            if keys[pygame.K_DOWN]:
                whiteBlock.rect.y +=1 
            if keys[pygame.K_LEFT]:
                whiteBlock.rect.x +=-1
            if keys[pygame.K_RIGHT]:
                whiteBlock.rect.x+=1  
            if keys[pygame.K_d]:
                greenBlock.dirty=1
            
            
            # blockGrp1.draw(self.screen)
            # blockGrp2.draw(self.screen)
            self.screen.fill(BLACK)
            group.draw(self.screen)
            
            

            pygame.display.flip()
            
            

game = GUI()

        