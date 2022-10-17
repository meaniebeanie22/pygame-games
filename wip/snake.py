import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

HEIGHT = 500
WIDTH = 500
FPS = 15
SPEED = 10
APPLES = 2 

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("An Abomination of Snake")

class Player(pygame.sprite.Sprite):
    def __init__(self): ## 
        super().__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect()
        self.pos = vec(WIDTH//2, HEIGHT//2)
        self.score = 1
        self.direction = 'up'
        all_sprites.add(self)
        self.cells = [self.pos]
        


    def move(self): ## 
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.direction = 'up'
        elif pressed_keys[K_RIGHT]:
            self.direction = 'right'
        elif pressed_keys[K_DOWN]:
            self.direction = 'down'
        elif pressed_keys[K_LEFT]:
            self.direction = 'left'

        if self.direction == 'up':
            self.pos.y -= SPEED
        elif self.direction == 'right':
            self.pos.x += SPEED
        elif self.direction == 'down':
            self.pos.y += SPEED
        elif self.direction == 'left':
            self.pos.x -= SPEED
        
        self.rect.center = self.pos

        # deal with cells
        self.cells.insert(0, self.pos)
        while len(self.cells) > self.score:
            self.cells.pop()
            
    def update(self):
        hits = pygame.sprite.spritecollide(self, apples, False)
        if hits:
            for apple in hits:
                self.score += 1
                apple.kill()
        


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (round(random.randint(10, WIDTH-10), -1), round(random.randint(10, HEIGHT-10), -1)))
        all_sprites.add(self)
    
    def move(self):
        pass

all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
def apple_gen():
    while len(apples) < APPLES:
        ap = Apple()
        apples.add(ap) 

P1 = Player()

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    apple_gen()

    if P1.pos.x > WIDTH or P1.pos.y > HEIGHT or P1.pos.x < 0 or P1.pos.y < 0:
        print('failure, score =', P1.score)
        break

    displaysurface.fill((0,0,0))

    for entity in all_sprites:
        if isinstance(entity, Player):
            print(entity.cells)
            for cell in entity.cells:
                sur = pygame.Surface((10,10))
                sur.fill((0,255,0))
                rec = sur.get_rect()
                rec.center = cell
                print(rec)
                displaysurface.blit(sur, rec)
        else:
            displaysurface.blit(entity.surf, entity.rect)
        
        entity.move()
        
    f = pygame.font.SysFont("Verdana", 20)     
    g  = f.render(str(P1.score), True, (123,255,0))   
    displaysurface.blit(g, (WIDTH/2, 10)) 

    pygame.display.update()
    FramePerSec.tick(FPS)
