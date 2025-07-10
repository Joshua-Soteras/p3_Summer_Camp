import pygame

#Helps to locate assets files dynamically/find file path automatically
import os
from os import listdir
from os.path import isfile, join 

from assets_Access.loadSpriteSheets import load_sprite_sheets

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
  
    
    #Animation Delay: takes into account for the shift in animations (changing sprites)
    ANIMATION_DELAY = 5

    #The width and height will be determinded by the image we are using for the player
    def __init__(self, x,y, width, height):

        super().__init__()

        #rect is just a tuple taking 4 values for arguemnts
        self.rect = pygame.Rect(x,y,width, height)
        self.SPRITES = load_sprite_sheets("MainCharacters" , "MaskDude", 32,  32, True)
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
