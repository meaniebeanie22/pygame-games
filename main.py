import pygame
from pygame.locals import *
import sys
 
pygame.init()
 
vec = pygame.math.Vector2 # 2d vector
HEIGHT = 450 # window dims
WIDTH = 400 # ""
ACC = 0.5 # char acceleration
FRIC = -0.12 # char friction
FPS = 60 # fps limit
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) # make a screen
pygame.display.set_caption("Game") # set title
 
class Player(pygame.sprite.Sprite): # player is a sprite
    def __init__(self): # init player
        super().__init__() # init player's sprite?
        self.surf = pygame.Surface((30, 30)) # make the surface that we use to represent the player (that is 30*30px)
        self.surf.fill((128,255,40)) # fill it in
        self.rect = self.surf.get_rect() # make a rectangle hitbox for it too
   
        self.pos = vec((10, 385)) # position as a vector - don't know entirely why tho
        self.vel = vec(0,0) # velocity as a vector
        self.acc = vec(0,0) # acceleration as a vector
 
    def move(self):
        self.acc = vec(0,0.5) # starting point for acceleration - no x and down 0.5 for y (for gravity)
    
        pressed_keys = pygame.key.get_pressed() # get pressed keys           
        if pressed_keys[K_LEFT]: # if left is pressed
            self.acc.x = -ACC # x acceleration = -ACC (ACC being a constant)
        if pressed_keys[K_RIGHT]: # if right is pressed
            self.acc.x = ACC # x acceleration = ACC (make us accelerate to the right)
             
        self.acc.x += self.vel.x * FRIC # allow us to alow down or speed up depending on acceleration
        self.vel += self.acc # add acceleration to velocity (duh that's how that works)
        self.pos += self.vel + 0.5 * self.acc # voodoo bullshit
         
        if self.pos.x > WIDTH: # if we go past the edge tp to other side (portal)
            self.pos.x = 0 # tp to other side
        if self.pos.x < 0: # if we go through the left border off the map
            self.pos.x = WIDTH # tp to otherside
            
        self.rect.midbottom = self.pos  # reference point for char = middle bottom of hitbox (for collisions)  
    
    def update(self): #update to make sure we not sad
        hits = pygame.sprite.spritecollide(P1 ,platforms, False) # get collisions
        if P1.vel.y > 0: # if we're moving
            if hits: # and there's any hits
                self.vel.y = 0 # then stop us
                self.pos.y = hits[0].rect.top + 1 # and move us to the top of the platform
     
    def jump(self): # jump 
        hits = pygame.sprite.spritecollide(self, platforms, False) # return platforms we're touching
        if hits: # if there are any, then we can jump
           self.vel.y = -15 # jump with 15u of beans
 
class platform(pygame.sprite.Sprite): # platforms are sprites
    def __init__(self): # make a platform
        super().__init__() # make the sprite to make the platform
        self.surf = pygame.Surface((WIDTH, 20)) # a platform is a surface
        self.surf.fill((255,0,0)) # fill it
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10)) # move it to a pos for testing
    
    def move(self): # placeholder to deal with scrolling
        pass

PT1 = platform() # pt1 is a plat
P1 = Player() # player is a player
 
platforms = pygame.sprite.Group() # make a group called platforms
platforms.add(PT1) # add test platform to it

all_sprites = pygame.sprite.Group() # make a group for our stuff
all_sprites.add(PT1) # add plat to it
all_sprites.add(P1) # add player to it
 
while True: # game loop
    for event in pygame.event.get(): # window exit logic
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    # if the player is pressing a key
            if event.key == pygame.K_SPACE: # is it space?
                P1.jump() # call the jump method
    

    displaysurface.fill((0,0,0)) # make the screen
    P1.update() # update the player for this frame

    for entity in all_sprites: # for all things
        displaysurface.blit(entity.surf, entity.rect) # draw them
        entity.move() # move the entity (if it can atm)
    
    pygame.display.update() # update the display
    FramePerSec.tick(FPS) # tick at ratelimit