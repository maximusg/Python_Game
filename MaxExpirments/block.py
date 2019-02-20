import pygame
from pygame.locals import *
from pygame.compat import geterror
from pathlib import *
import os

# Define some colors
# BLACK = (  0,   0,   0)
# WHITE = (255, 255, 255)
# RED   = (255,   0,   0)

class Block(pygame.sprite.DirtySprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
   def __init__(self, group, color, width,  height, layer):
       # Call the parent class (Sprite) constructor
       #This is the way pygame does it
      # super().__init__(self, group) #Best practice

      # Create an image of the block, and fill it with a color.
      # This could also be an image loaded from the disk.
      self.image = pygame.Surface([width, height])
      self.image.fill(color)
      self.dirty=1
      self._layer = layer
      pygame.sprite.Sprite.__init__(self,group)
      

      # Fetch the rectangle object that has the dimensions of the image
      # Update the position of this object by setting the values of rect.x and rect.y
      self.rect = self.image.get_rect()
       
  


      
        