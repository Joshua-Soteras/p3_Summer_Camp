import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 

from game_Objects.gameObject import Object


#Size that is being passed in the size of the block/sprite
def get_block(size):

    #Path to the assets of the block terrain
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()

    #Create an image of that size (of what is passed in)
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    
    #Loading the location of the specific platform panel/sprite we want
    #If want the load a different platform sprite we have to set the coorect coordinates
    rect = pygame.Rect(96, 0, size, size)

    #Draw this image on the surface 
    surface.blit(image, (0,0), rect)

    #Scale it to be larger
    return pygame.transform.scale2x(surface)

#-------------------------------------------------
#BLOCK: platform

class Block(Object):

    #block is only one size thus no width/height
    def __init__(self, x, y, size):

        super().__init__(x, y, size, size)

        #load the block image/sprite
        block = get_block(size)

        #draw the block at position 0 , 0 
        self.image.blit(block, (0,0))

        self.mask = pygame.mask.from_surface(self.image)







