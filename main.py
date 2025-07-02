import random 
import math 
import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 

#Initialize the Pygame Module 
pygame.init()
#Set the caption at the top of the window 
pygame.display.set_caption("Platformer")


#-------------------------------------------------
#GLOBAL VARIABLES: Setting up the game

#Background color / RGB Parameters 
#BG_COLOR = (255,255,255)

#Width and Height of the Screen
WIDTH, HEIGHT = 800, 800

#Frame Per Second
FPS = 60

#Player Speed: 
PLAYER_VEL = 5

#Size of the game window 
window = pygame.display.set_mode((WIDTH, HEIGHT))



#-------------------------------------------------
#PLAYER CREATION

#questions for these functions
#self.pygameRect
#self.pygame.draw.rect
#window.blit
pygame.sprite.Sprite

class Player(pygame.sprite.Sprite):

    COLOR = (255, 0 ,0)
    #If we have two sprites we can use this method to do collision
    
    #The width and height will be determinded by the image we are using for the player
    def __init__(self, x,y, width, height):

        #rect is just a tuple taking 4 values for arguemnts
        self.rect = pygame.Rect(x,y,width, height)
        
        #How fast we are moving the player in both directions
        #apply velocity until we remove that velocity
        self.x_vel = 0
        self.y_vel = 0 

        #
        self.mask = None

        #Animations for direction
        #Keeping track of direction the player is facing
        self.direction = "left"
        #Resetting the count when changing directions makes it smoother when resetting
        self.animation_count = 0 


    #Moving Function
    #Parameters: Taking displacement in x direction and y direction
    def move(self, dx,dy):

        self.rect.x += dx
        self.rect.y += dy
    
    #Move Left Direction
    def move_left(self, vel):
        
        #Using negative value to move in opposite direction
        #Refer to the coordinate system of pygame
        self.x_vel = - vel

        #Changes Direction of Sprite/Player
        if self.direction != "left": 
            self.direction = "left"
            self.animation_count = 0

    #Move Right Direction
    def move_right(self, vel):

        #Using positive value to move in opposite direction
        #Refer to the coordinate system of pygame
        self.x_vel = vel

        #Changes Direction of Sprite/Player
        if self.direction != "right": 
            self.direction = "right"
            self.animation_count = 0
    
    #Call once every frame (one iteration of the while loop)
    #Handles all the updates: movements, animations, etc.
    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)




#-------------------------------------------------
#BACKGROUND CREATION

#List of all the Tiles that need to be drawn
#Run in the same dir as the assets folder
def get_background(name):

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


def draw (window, background, bg_image, player): 

    #Loop through all the tiles we have and drawing them
    for tile in background: 
        #Parameters
        #bg_image: the image we want to draw
        #tile: the position we are drawing the title at 
        window.blit(bg_image, tile)
    
    #drawing the player
    player.draw(window)

    #update the screen every second 
    pygame.display.update()



#-------------------------------------------------
#STARTING THE GAME

#Main function starts the game 
#Main handles the "event loop" : updating the games constantly
def main(window):

    clock = pygame.time.Clock()

    background , bg_image = get_background("Blue.png")

    #Player Creation: See Class
    player = Player(100,100, 50,50)


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

        draw(window, background, bg_image, player)

    #Closes the Game
    pygame.quit()
    quit()

#Runs Game Code / Only call the main function if we call this file directly 
if __name__ == "__main__":
    main(window)

