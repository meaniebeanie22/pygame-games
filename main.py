# begin with jump test
from curses import KEY_UP
import sys, pygame
pygame.init()

size = width, height = 640, 480
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1: #game loop
    for event in pygame.event.get(): # if quit window then stop
        if event.type == pygame.QUIT: sys.exit()
    
    if (pygame.key.getpressed()[pygame.K_UP]):
        print('up key pressed')

    # start drawing the next screen
    screen.fill(black) # make the screen blank
    screen.blit(ball, ballrect) # draw on the rectangle in its new location
    pygame.display.flip() # show new screen