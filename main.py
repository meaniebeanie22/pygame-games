
import pygame # import
pygame.init() # init

win = pygame.display.set_mode((500,500)) # make display
pygame.display.set_caption("First Game") # set title

# init vars for player
x = 250 # starting screen pos for player
y = 400 # ""
width = 20 # width of player
height = 30 # height of player
vel = 5 # steps per tick of move

# init vars for testing platform
platX = 350
platY = 300
platWidth = 125
platHeight = 20

# list of platform objects
platforms = [pygame.Rect(platX,platY,platWidth,platHeight)]

isJump = False # keeps track of jumping
jumpCount = 10 # has to do with jump height

run = True

while run:
    pygame.time.delay(25) # time per frame

    for event in pygame.event.get(): # exiting program
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed() # get keypresses
    
    if keys[pygame.K_LEFT] and x > vel: # make sure no go out of bounding box x left - will not need later on
        x -= vel

    if keys[pygame.K_RIGHT] and x < 500 - vel - width:  # make sure no go out of bounding box right - will not need later on
        x += vel
        
    if not(isJump): # can jump if not already jumping
        if keys[pygame.K_UP]:
            isJump = True
    else: # jump logic
        
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 10
            isJump = False
    
    # draw next frame
    win.fill((0,0,0)) # bg
    pygame.draw.rect(win, (255,0,0), (x, y, width, height)) # player

    for plat in platforms: # draw all platforms
        pygame.draw.rect(win, (0,125,255), plat)

    pygame.display.update() 
    
pygame.quit()