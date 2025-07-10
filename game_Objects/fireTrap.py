import pygame 
from assets_Access.loadSpriteSheets import load_sprite_sheets
from game_Objects.gameObject import Object

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
