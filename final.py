## add the ability to get a spare life, that is used when you fall into the void and yeets you back up again - square is yellow without a life and purple with one
## spare life spent when touch tile and not used

import pygame
from pygame.locals import *
import sys
import random
import time
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 500
WIDTH = 1080
ACC = 0.35
FRIC = -0.12
FPS = 120

 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
        self.safe = False
 
    def move(self):
        self.acc = vec(0,0.2)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -11
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1
                    if hits[0].special == True:
                            if self.safe == False:
                                hits[0].special = False
                                hits[0].surf.fill((0,255,0))
                                self.safe = True          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
        if self.safe:
            self.surf.fill((138,43,226))
        else:
            self.surf.fill((255,255,0))
 
P1 = Player()

class platform(pygame.sprite.Sprite): ## rand gen ok
    def __init__(self):
        super().__init__()
        self.special = False
        self.surf = pygame.Surface((random.randint(50,100), 20))
        if random.randint(1,P1.score//2+10) == 1: # special tile
            self.surf.fill((255,0,255))
            self.special = True
        else:
            self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(spawnbox.left, WIDTH-10),
                                                 random.randint(spawnbox.top+120, spawnbox.bottom - 120))) 
        self.point = True
    
    def move(self):
        pass
 
 
def check(platform, groupies): ## and fix checking
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 100) and (abs(platform.rect.bottom - entity.rect.top) < 100) and (abs(platform.rect.right - entity.rect.left) < 150) and (abs(platform.rect.left - entity.rect.right) < 150):
                return False
        C = False
 
def plat_gen(): ## fix generation using spawnbox
    while len(spawnbox.collidelistall(platforms.sprites())) < 1:
        width = random.randrange(20,50)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(spawnbox.left + 150, WIDTH - width),
                              random.randrange(spawnbox.top, spawnbox.bottom - 20))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
spawnbox = Rect(3*WIDTH//4, 100, WIDTH//4, HEIGHT-100) # make sure there are n platforms in here at all times
        
PT1 = platform() # spawn plat
PT1.special = False
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.point = False   ##
# init gen
for x in range(random.randint(1,2)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
 
while True:
    ##
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_UP:
                P1.cancel_jump()
    
    if pygame.key.get_pressed()[pygame.K_UP] == True:
            P1.jump()
 
    if P1.rect.right >= WIDTH / 2 : ## need to be changed for horizontal/ has been changed
        distover = P1.rect.right - WIDTH / 2
        P1.pos.x -= distover #abs(P1.vel.x) better idea find distance over, then move back, and move the plats back by same amount
        for plat in platforms: ##
            plat.rect.x -= distover ##
            if plat.rect.right <= 0: ##
                plat.kill() ##

    if P1.rect.top > HEIGHT: ## GOOD DON'T CHANGE!!!
        if P1.safe == True:
            P1.pos.y = HEIGHT - 1
            P1.vel.y = -11
            P1.safe = False
        else:
            print('fail') ## beans
            time.sleep(1)
            break
 
    plat_gen()
    displaysurface.fill((0,0,0))
    f = pygame.font.SysFont("Verdana", 20)     
    g  = f.render(str(P1.score), True, (123,255,0))   
    displaysurface.blit(g, (WIDTH/2, 10))   
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS)