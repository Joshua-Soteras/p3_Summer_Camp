import pygame

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