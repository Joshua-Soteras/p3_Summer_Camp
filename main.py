import random 
import math 
import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 


#Character Modules
from player import Player
from player_Actions import handle_move

#Terrain 
from assets_Access.background import get_background
from game_Objects.block import Block

#Object(s)
from game_Objects.fireTrap import Fire


#-------------------------------------------------
#GLOBAL VARIABLES: Setting up the game

#Background color / RGB Parameters 
#BG_COLOR = (255,255,255)

#Width and Height of the Screen
WIDTH, HEIGHT = 1000, 1000

#Frame Per Second
FPS = 60

#Player Speed: 
PLAYER_VEL = 6


#Initialize the Pygame Module 
pygame.init()
#Set the caption at the top of the window 
pygame.display.set_caption("Platformer")
#Size of the game window            
window = pygame.display.set_mode((WIDTH, HEIGHT))



#-------------------------------------------------
#Drawing/Rendering all images (method)
#offset_x is for screen scrolling
def draw(window, background, bg_image, player, objects, offset_x): 

    #Loop through all the tiles we have and drawing them
    for tile in background: 
        #Parameters
        #bg_image: the image we want to draw
        #tile: the position we are drawing the title at 
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x)

    #drawing the player
    player.draw(window, offset_x)

    #update the screen every second 
    pygame.display.update()



#-------------------------------------------------
#STARTING THE GAME

#Main function starts the game 
#Main handles the "event loop" : updating the games constantly
def main(window):

    clock = pygame.time.Clock()

    #Getting Background
    background , bg_image = get_background("Blue.png", WIDTH, HEIGHT)

    #Player Creation: See Class
    player = Player(100, 100, 50, 50)

    #Creating the Terrain
    block_size = 96
    #Some going to left and right
    #-WIDTH // block_size -> how many blocks to the left
    #i is it the x coordinate where to place the block 
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size, (WIDTH *2) // block_size )]
    

    #Creating Fire
    fire = Fire(100, HEIGHT - block_size -64, 16, 32)
    fire.on()

    #*floor grabs all individual floor elements
    #Basically doing what is above with floor
    #block(0, HEIGHT - block_size * 2, y axis
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size),
               fire]


    #For Screen Scrolling/See within run loop
    offset_x = 0
    #When the player gets 200 pixels to left or the right of the screen, the screen starts scrolling
    scroll_area_width = 200
    

    #This will act as our "event loop"
    run = True
    while run: 

        #Ensures that our while loop runs at the set FPS
        clock.tick(FPS)

        for event in pygame.event.get():

            #First Event: Checking if user quits
            if event.type == pygame.QUIT:
                run = False
                break
                #probably can improve in closing the gmae

            #Jumping keys 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        #Updates of the players movement
        #Loop moves the character depending on the x and  vel set 
        player.loop(FPS)
        fire.loop() #Updates Fire Animation

        #Handling Player Inputs + Collision of player
        handle_move(player, objects, PLAYER_VEL)

        #Rendering 
        draw(window, background, bg_image, player, objects, offset_x)

        #Screen Scrolling
        #Starting Scrolling when Player Starts getting to the edge / boundary
        #Checking if moving to the right
        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel >0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel <0):
            offset_x += player.x_vel



    #Closes the Game
    pygame.quit()
    quit()

#Runs Game Code / Only call the main function if we call this file directly 
if __name__ == "__main__":
    main(window)

