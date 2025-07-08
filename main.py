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

        #For Pixels of the Character and use for Collision
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

        #Character Getting Hit
        self.hit = False
        self.hit_count = 0 

    
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

    def make_hit(self):
        self.hit = True
        self.hit_count = 0 

            
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

        #Registering Hits and Animation
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

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

        #Getting Hit
        if self.hit:
            sprite_sheet = "hit"

        #Jumping Animation: Single and Double Jump
        elif self.y_vel < 0:
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


    def draw(self, win, offset_x):
       
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))



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
    
    def draw(self, win, offset_x) :
        win.blit(self.image, (self.rect.x -offset_x, self.rect.y))


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


class Fire(Object):

    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):

        #Name is fire, we can determine if we collide with it
        super().__init__( x, y, width, height, "fire")

        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
       
        #Animation anme is either on or off
        sprites = self.fire[self.animation_name]
        
        #Every animtiondelay value frames we want to show a slight lag for animations
        #If we have 5 (animation delay) sprites and we are on count 10, we are showing the 2nd animation
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        #Select the sprite animation we have available
        self.image = sprites[sprite_index]
        self.animation_count +=1

        #sconstantly adjust the rectangle to what the rectangle we have already
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        #mask is a mapping of all the pixels that exist within the sprite
        #pixel perfect pixel image/ collides where there are pixels
        #this is better than rectangluar collision : looks like we are hitting without touching
        self.mask = pygame.mask.from_surface(self.image)

        #Adjusting Animation Count: Don't want it to become a big numnber since the fire is static
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0



#-------------------------------------------------
#MOVING and COLLISION : Handling player inputs and collision

#the player and the list of objects we can be colliding with
def handle_move(player , objects):
    keys = pygame.key.get_pressed()

    #Player keeps move while holding down
    #becomes zero if not moving 
    player.x_vel = 0

    #Horizonzantal Collision
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, -PLAYER_VEL * 2)

    #Tells if the key is pressed
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    
    vertical_collide = hande_vertical_collision(player, objects, player.y_vel)
    #All the objects we collided with
    to_check = [collide_left, collide_right, *vertical_collide]

    #If anything of them is fire we say we got hit by the fire
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

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

            #Moving up / Colliding witha cieling or upper object
            elif dy < 0 : 
                player.rect.top = obj.rect.bottom
                player.hit_head()
        
            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):

    #Checking if player were to move to the right/left would they hit an object
    player.move(dx,0)

    #Update the Rectangle and maskbefore we check collision
    player.update()

    #Then we check if our rectangle/mask is colliding with an object(s)
    collided_objects = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_objects = obj
            break

    #Move the player back where they are originally 
    player.move(-dx, 0)

    #Update Mask/Rectangle Again
    player.update()

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
        handle_move(player, objects)

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

