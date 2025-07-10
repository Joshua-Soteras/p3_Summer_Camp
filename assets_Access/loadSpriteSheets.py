import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 


#-------------------------------------------------
#SPRITE HANDLING

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


#Chooses which Sprite Sheet to use: jumping, running, etc
#Parameters: dir1: characters, dir2: others, width and height: of image
#direction if there a multiple directions
def load_sprite_sheets(dir1, dir2, width, height , direction = False):
    path = join("assets", dir1, dir2)

    #Get all images in directory 
    images = [f for f in listdir(path) if isfile(join(path,f))]

    #Dictionary: key = animation style / value = sprite 
    all_sprites = {}

    for image in images:
        
        # individual image sheet with transparent background
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        #Get all the invidiual sprites from the image
        sprites = []

        #width of the individual image within the sprite sheet 
        for i in range(sprite_sheet.get_width() // width):

            #32 is the depth
            #This surface is where we will be "Drawing" or bliting the imagge
            surface = pygame.Surface((width, height) , pygame.SRCALPHA , 32)

            #The frame that we will draw onto the surface
            rect = pygame.Rect(i* width, 0, width, height)
            surface.blit(sprite_sheet, (0,0) , rect)
            #32x32 to 64x64
            sprites.append(pygame.transform.scale2x(surface))

            if direction: 
                all_sprites[image.replace(".png" , "") + "_right"] = sprites
                all_sprites[image.replace(".png" , "") + "_left"] = flip(sprites)

            else: 
                all_sprites[image.replace(".png" , "")] =sprites
        
    return all_sprites