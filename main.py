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
#PLAYER CREATION (Class)

#questions for these functions
#self.pygameRect
#self.pygame.draw.rect
#window.blit
#pygame.sprite.Sprite

class Player(pygame.sprite.Sprite):

    COLOR = (255, 0 ,0)

    #Larger Values makes gravity "faster"
    GRAVITY = 1

    #Sprite for player character
    #true for multidirectional sprite / left and right
    SPRITES = load_sprite_sheets("MainCharacters" , "MaskDude", 32,  32, True)
    
    #Animation Delay: takes into account for the shift in animations (changing sprites)
    ANIMATION_DELAY = 5

    #The width and height will be determinded by the image we are using for the player
    def __init__(self, x,y, width, height):

        super().__init__()

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

        #Tells us how long we've been falling
        self.fall_count = 0 

        #Jumping
        self.jump_count = 0

    
    #Jumping Method
    def jump(self):

        #-Gravity * how fast
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        
        #As soon as player jumps, get rid of accumalted gravity
        #Only for the first jump
        if self.jump_count == 1:
            self.fall_count == 0 

            
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

        #Simulating Gravity
        #Add velocity to the y_vel: min being 1
        #FLAG: LOOK MORE INTO THIS
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)

        #Updating the velocity of the character
        self.move(self.x_vel, self.y_vel)

        #Updating Fall Time
        #NoteL once this is 60 -> 60 /fps = 60/60 = 1 sec of fall time
        self.fall_count += 1
        self.update_sprite()
    
    #Collision
    def landed(self):
        #reset the falling/ adding gravity.
        self.fall_count = 0
        #reseting velocity
        self.y_vel = 0 
        #for doubling jumping
        self.jump_count = 0

    #Collision
    def hit_head(self):
        self.count = 0
        #reverse the velocity / bounce of the block and start falling
        self.y_vel *= -1


    #Animations for player character
    def update_sprite(self):

        #Default animation
        sprite_sheet = "idle"

        #Jumping Animation: Single and Double Jump
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        
        #Falling Animation
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"

        #Running Animation
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        
        #Every animtiondelay value frames we want to show a slight lag for animations
        #If we have 5 (animation delay) sprites and we are on count 10, we are showing the 2nd animation
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        #Select the sprite animation we have available
        self.sprite = sprites[sprite_index]
        self.animation_count +=1
        self.update()
    

    #Udpate the bounding box of our sprite model
    #Want to have the same size of the sprite we have
    #All sprites have different sizes
    def update(self): 
        #constantly adjust the rectangle to what the rectangle we have already
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        
        #mask is a mapping of all the pixels that exist within the sprite
        #pixel perfect pixel image/ collides where there are pixels
        #this is better than rectangluar collision : looks like we are hitting without touching
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win):
       
        win.blit(self.sprite, (self.rect.x, self.rect.y))



#-------------------------------------------------
#OBJECTS : objects in screen

#Base Class for all objects in the game 
#All properites for a base object in the game
class Object(pygame.sprite.Sprite): 

    def __init__(self,x, y, width, height, name=None):

        super().__init__()

        #For object.
        self.rect = pygame.Rect(x, y, width, height)

        #Transparent Images
        self.image = pygame.Surface((width, height) , pygame.SRCALPHA)

        #height / widths
        self.width = width
        self.height = height

        #name of sprite
        self.name = name
    
    def draw(self,win):
        win.blit(self.image, (self.rect.x, self.rect.y))


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

    

#-------------------------------------------------
#MOVING and COLLISION : Handling player inputs and collision

#the player and the list of objects we can be colliding with
def handle_move(player , objects):
    keys = pygame.key.get_pressed()

    #Player keeps move while holding down
    #becomes zero if not moving 
    player.x_vel = 0

    #Tells if the key is pressed
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)
    
    hande_vertical_collision(player, objects, player.y_vel)


def hande_vertical_collision(player, objects, dy):

    collided_objects = []

    for obj in objects:

        #refer to the mask property to why collison works
        if pygame.sprite.collide_mask(player, obj):
            
            #If moving down, then colliding ontop of object
            if dy > 0:
                #Bottom of the character on top of the object
                player.rect.bottom = obj.rect.top
                player.landed()

            #Moving up
            elif dy < 0 : 
                player.rect.top = obj.rect.bottom
                player.hit_head()
        
        collided_objects.append(obj)

    return collided_objects



#-------------------------------------------------
#BACKGROUND CREATION (method)

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



#-------------------------------------------------
#Drawing/Rendering all images (method)
def draw(window, background, bg_image, player, objects): 

    #Loop through all the tiles we have and drawing them
    for tile in background: 
        #Parameters
        #bg_image: the image we want to draw
        #tile: the position we are drawing the title at 
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window)

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
    player = Player(100, 100, 50, 50)


    #Creating the Terrain
    block_size = 96

    #Some going to left and right
    #-WIDTH // block_size -> how many blocks to the left
    #i is it the x coordinate where to place the block 
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size, (WIDTH *2) // block_size )]


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

        #Handling Player Inputs + Collision of player
        handle_move(player, floor)

        #Rendering 
        draw(window, background, bg_image, player, floor)

    #Closes the Game
    pygame.quit()
    quit()

#Runs Game Code / Only call the main function if we call this file directly 
if __name__ == "__main__":
    main(window)

