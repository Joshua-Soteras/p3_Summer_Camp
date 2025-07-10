import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 
#-------------------------------------------------
#BACKGROUND CREATION (method)

#List of all the Tiles that need to be drawn
#Run in the same dir as the assets folder
def get_background(name, WIDTH, HEIGHT):

    #Creating the file path to grab the tile from assets folder
    image = pygame.image.load(join("assets", "Background", name))

    #x, y, width, height of the title
    _, _, width, height = image.get_rect()

    tiles = []

    #for loop to create x (i) and y (j) directions
    #WIDTH of screen // width of tile 
    for i in range (WIDTH // width +1):

        for j in range(HEIGHT // height +1):

            #denotes the top corner of the screen
            #tuple
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image