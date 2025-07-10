import pygame 
#-------------------------------------------------
#MOVING and COLLISION : Handling player inputs and collision

#the player and the list of objects we can be colliding with
def handle_move(player , objects , PLAYER_VEL):
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
    
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    #All the objects we collided with
    to_check = [collide_left, collide_right, *vertical_collide]

    #If anything of them is fire we say we got hit by the fire
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def handle_vertical_collision(player, objects, dy):

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
