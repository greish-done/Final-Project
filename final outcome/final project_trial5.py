import random, sys, time, math, pygame
from pygame.locals import *

FPS = 30
WINWIDTH = 900
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

WATERCOLOR = (150, 220, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

CAMERASLACK = 90
MOVERATE = 9
BOUNCERATE = 30
BOUNCEHEIGHT = 25
STARTSIZE = 50
WINSIZE = 200
INVULNTIME = 2
MAXHEALTH = 3

NUMREEF = 80
NUMSTINGRAYS = 4
NUMTURTLES = 5
NUMCRABS = 5
NUMWHALES = 3
NUMNEMOS = 6
NUMSQUIDS = 4
MINSPEED = 4
MAXSPEED = 6
DIRCHANGEFREQ = 2
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, L_WHALE_IMG, R_WHALE_IMG,\
        R_STINGRAY_IMG, L_STINGRAY_IMG, R_TURTLE_IMG, L_TURTLE_IMG, R_CRAB_IMG,\
            L_CRAB_IMG, R_KWHALE_IMG, L_KWHALE_IMG, R_NEMO_IMG, L_NEMO_IMG,\
                R_SQUID_IMG, L_SQUID_IMG, REEFIMAGES

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Marine Ecosystem')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # load the image files
    L_WHALE_IMG = pygame.image.load('범고래_main.png')
    R_WHALE_IMG = pygame.transform.flip(L_WHALE_IMG, True, False)
    R_STINGRAY_IMG = pygame.image.load('sealife1.png')
    L_STINGRAY_IMG = pygame.transform.flip(R_STINGRAY_IMG, True, False)
    R_TURTLE_IMG = pygame.image.load('sealife2.png')
    L_TURTLE_IMG = pygame.transform.flip(R_TURTLE_IMG, True, False)
    R_CRAB_IMG = pygame.image.load('sealife3.png')
    L_CRAB_IMG = pygame.transform.flip(R_CRAB_IMG, True, False)
    R_KWHALE_IMG = pygame.image.load('sealife4.png')
    L_KWHALE_IMG = pygame.transform.flip(R_KWHALE_IMG, True, False)
    R_NEMO_IMG = pygame.image.load('sealife5.png')
    L_NEMO_IMG = pygame.transform.flip(R_NEMO_IMG, True, False)
    R_SQUID_IMG = pygame.image.load('sealife6.png')
    L_SQUID_IMG = pygame.transform.flip(R_SQUID_IMG, True, False)
    REEFIMAGES = []
    for i in range(1, 9):
        REEFIMAGES.append(pygame.image.load('bg_bubble%s.png' % i))

    while True:
        show_start_screen()
        runGame()


def show_start_screen():
        # game splash/start screen
        pygame.mixer.music.load('Under The Sea.mp3')
        pygame.mixer.music.play(loops=-1)
        DISPLAYSURF.fill(WATERCOLOR)
        DISPLAYSURF.blit(background, background_rect)
        draw_text("Under the Sea", 48, BLACK, WINWIDTH / 2, WINHEIGHT * 2 / 9)
        draw_text("Arrows to move", 20, BLACK, WINWIDTH / 2, WINHEIGHT * 4 / 9)
        draw_text("Press a key to play", 22, BLACK, WINWIDTH / 2, WINHEIGHT * 3 / 5)
        pygame.display.flip()
        wait_for_key()
        pygame.mixer.music.fadeout(500)

# Load game graphics
background = pygame.image.load('시작화면 배경.png')
background_rect = background.get_rect()


def runGame():
    # set up variables for the start of a new game
    invulnerableMode = False
    invulnerableStartTime = 0
    gameOverMode = False
    winMode = False

    # sound play
    pygame.mixer.music.load('Bubble.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)    

    # create the surfaces to hold game text
    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    gameOverSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
    gameOverRect2 = gameOverSurf2.get_rect()
    gameOverRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)

    winSurf = BASICFONT.render('You became a predator of the sea!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)

    camerax = 0
    cameray = 0

    reefObjs = []
    stingrayObjs = []
    turtleObjs = []
    crabObjs = []
    whaleObjs = []
    nemoObjs = []
    squidObjs = []

    # stores the player object:
    playerObj = {'surface': pygame.transform.scale(L_WHALE_IMG, (STARTSIZE, STARTSIZE)),
                 'facing': LEFT,
                 'size': STARTSIZE,
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'bounce':0,
                 'health': MAXHEALTH}

    moveLeft  = False
    moveRight = False
    moveUp    = False
    moveDown  = False

    # start off with some random coral reef images on the screen
    for i in range(10):
        reefObjs.append(makeNewReef(camerax, cameray))
        reefObjs[i]['x'] = random.randint(0, WINWIDTH)
        reefObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True: # main game loop
        # Check if we should turn off invulnerability
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        # move all the marine lives
        for sObj in stingrayObjs:
            # move the stingray, and adjust for their bounce
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0 # reset bounce amount

            # random chance they change direction
            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity() - 1
                sObj['movey'] = getRandomVelocity() + 3
                if sObj['movex'] > 0: # faces right
                    sObj['surface'] = pygame.transform.scale(R_STINGRAY_IMG, (sObj['width'], sObj['height']))
                else: # faces left
                    sObj['surface'] = pygame.transform.scale(L_STINGRAY_IMG, (sObj['width'], sObj['height']))

        for sObj in turtleObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity() - 3
                sObj['movey'] = getRandomVelocity() - 3
                if sObj['movex'] > 0:
                    sObj['surface'] = pygame.transform.scale(R_TURTLE_IMG, (sObj['width'], sObj['height']))
                else:
                    sObj['surface'] = pygame.transform.scale(L_TURTLE_IMG, (sObj['width'], sObj['height']))
        
        for sObj in crabObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ + 10:
                sObj['movex'] = getRandomVelocity() + 2
                sObj['movey'] = getRandomVelocity()
                if sObj['movex'] > 0:
                    sObj['surface'] = pygame.transform.scale(R_CRAB_IMG, (sObj['width'], sObj['height']))
                else:
                    sObj['surface'] = pygame.transform.scale(L_CRAB_IMG, (sObj['width'], sObj['height']))

        for sObj in whaleObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ - 1:
                sObj['movex'] = getRandomVelocity() - 2
                sObj['movey'] = getRandomVelocity() - 3
                if sObj['movex'] > 0:
                    sObj['surface'] = pygame.transform.scale(R_KWHALE_IMG, (sObj['width'], sObj['height']))
                else:
                    sObj['surface'] = pygame.transform.scale(L_KWHALE_IMG, (sObj['width'], sObj['height']))

        for sObj in nemoObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity() + 8
                sObj['movey'] = getRandomVelocity() + 2
                if sObj['movex'] > 0:
                    sObj['surface'] = pygame.transform.scale(R_NEMO_IMG, (sObj['width'], sObj['height']))
                else:
                    sObj['surface'] = pygame.transform.scale(L_NEMO_IMG, (sObj['width'], sObj['height']))

        for sObj in squidObjs:
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate']:
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ:
                sObj['movex'] = getRandomVelocity() - 1
                sObj['movey'] = getRandomVelocity() - 1
                if sObj['movex'] > 0:
                    sObj['surface'] = pygame.transform.scale(R_SQUID_IMG, (sObj['width'], sObj['height']))
                else:
                    sObj['surface'] = pygame.transform.scale(L_SQUID_IMG, (sObj['width'], sObj['height']))


        # go through all the objects and see if any need to be deleted.
        for i in range(len(reefObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, reefObjs[i]):
                del reefObjs[i]
        for i in range(len(stingrayObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, stingrayObjs[i]):
                del stingrayObjs[i]
        for i in range(len(turtleObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, turtleObjs[i]):
                del turtleObjs[i]
        for i in range(len(crabObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, crabObjs[i]):
                del crabObjs[i]
        for i in range(len(whaleObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, whaleObjs[i]):
                del whaleObjs[i]
        for i in range(len(nemoObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, nemoObjs[i]):
                del nemoObjs[i]
        for i in range(len(squidObjs) - 1, -1, -1):
            if isOutsideActiveArea(camerax, cameray, squidObjs[i]):
                del squidObjs[i]


        # add more coral reefs & squirrels if we don't have enough.
        while len(reefObjs) < NUMREEF:
            reefObjs.append(makeNewReef(camerax, cameray))
        while len(stingrayObjs) < NUMSTINGRAYS:
            stingrayObjs.append(makeNewStingray(camerax, cameray))
        while len(turtleObjs) < NUMTURTLES:
            turtleObjs.append(makeNewTurtle(camerax, cameray))
        while len(crabObjs) < NUMCRABS:
            crabObjs.append(makeNewCrab(camerax, cameray))
        while len(whaleObjs) < NUMWHALES:
            whaleObjs.append(makeNewWhale(camerax, cameray))
        while len(nemoObjs) < NUMNEMOS:
            nemoObjs.append(makeNewNemo(camerax, cameray))
        while len(squidObjs) < NUMSQUIDS:
            squidObjs.append(makeNewSquid(camerax, cameray))
        

        # adjust camerax and cameray if beyond the "camera slack"
        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
            camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
            camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
            cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
            cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT

        # draw the skyblue background
        DISPLAYSURF.fill(WATERCOLOR)

        # draw all the coral reef objects on the screen
        for gObj in reefObjs:
            gRect = pygame.Rect( (gObj['x'] - camerax,
                                  gObj['y'] - cameray,
                                  gObj['width'],
                                  gObj['height']) )
            DISPLAYSURF.blit(REEFIMAGES[gObj['reefImage']], gRect)


        # draw the other marine lives
        for sObj in stingrayObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        for sObj in turtleObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        for sObj in crabObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        for sObj in whaleObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        for sObj in nemoObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])

        for sObj in squidObjs:
            sObj['rect'] = pygame.Rect( (sObj['x'] - camerax,
                                         sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                         sObj['width'],
                                         sObj['height']) )
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])


        # draw the player whale
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj['rect'] = pygame.Rect( (playerObj['x'] - camerax,
                                              playerObj['y'] - cameray - getBounceAmount(playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
                                              playerObj['size'],
                                              playerObj['size']) )
            DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])


        # draw the health meter
        drawHealthMeter(playerObj['health'])

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                    if playerObj['facing'] != LEFT: # change player image
                        playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    if playerObj['facing'] != RIGHT: # change player image
                        playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = RIGHT
                elif winMode and event.key == K_r:
                    return
                elif gameOverMode and event.key == K_r:
                    return

            elif event.type == KEYUP:
                # stop moving the player whale
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    terminate()

        if not gameOverMode:
            # actually move the player
            if moveLeft:
                playerObj['x'] -= MOVERATE
            if moveRight:
                playerObj['x'] += MOVERATE
            if moveUp:
                playerObj['y'] -= MOVERATE
            if moveDown:
                playerObj['y'] += MOVERATE

            if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                playerObj['bounce'] += 1

            if playerObj['bounce'] > BOUNCERATE:
                playerObj['bounce'] = 0 # reset bounce amount

            # check if the player has collided with any marine lives
            for i in range(len(stingrayObjs)-1, -1, -1):
                sqObj = stingrayObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del stingrayObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"

            for i in range(len(turtleObjs)-1, -1, -1):
                sqObj = turtleObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del turtleObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"

            for i in range(len(crabObjs)-1, -1, -1):
                sqObj = crabObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del crabObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"

            for i in range(len(whaleObjs)-1, -1, -1):
                sqObj = whaleObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del whaleObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"

            for i in range(len(nemoObjs)-1, -1, -1):
                sqObj = nemoObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del nemoObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"

            for i in range(len(squidObjs)-1, -1, -1):
                sqObj = squidObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/marine life collision has occurred

                    if sqObj['width'] * sqObj['height'] <= playerObj['size']**2:
                        # player is larger and eats the marine life
                        playerObj['size'] += int( (sqObj['width'] * sqObj['height'])**0.2 ) + 1
                        del squidObjs[i]

                        if playerObj['facing'] == LEFT:
                            playerObj['surface'] = pygame.transform.scale(L_WHALE_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT:
                            playerObj['surface'] = pygame.transform.scale(R_WHALE_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE:
                            winMode = True # turn on "win mode"

                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
                            gameOverMode = True # turn on "game over mode"
        else:
            # game is over, show "game over" text
            DISPLAYSURF.blit(gameOverSurf, gameOverRect)
            DISPLAYSURF.blit(gameOverSurf2, gameOverRect2)

        # check if the player has won.
        if winMode:
            DISPLAYSURF.blit(winSurf, winRect)
            DISPLAYSURF.blit(winSurf2, winRect2)
            invulnerableMode = True
            gameOverMode = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)


def terminate():
    pygame.quit()
    sys.exit()


def getBounceAmount(currentBounce, bounceRate, bounceHeight):
    return int(math.sin( (math.pi / float(bounceRate)) * currentBounce ) * bounceHeight)

def getRandomVelocity():
    speed = random.randint(MINSPEED, MAXSPEED)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed


def getRandomOffCameraPos(camerax, cameray, objWidth, objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect(camerax, cameray, WINWIDTH, WINHEIGHT)
    while True:
        x = random.randint(camerax - WINWIDTH, camerax + (2 * WINWIDTH))
        y = random.randint(cameray - WINHEIGHT, cameray + (2 * WINHEIGHT))
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect):
            return x, y


def makeNewStingray(camerax, cameray):
    sr = {}
    generalSize = random.randint(10, 30)
    multiplier = random.randint(2, 3)
    sr['width']  = (generalSize + random.randint(20, 30)) * multiplier
    sr['height'] = (generalSize + random.randint(20, 30)) * multiplier
    sr['x'], sr['y'] = getRandomOffCameraPos(camerax, cameray, sr['width'], sr['height'])
    sr['movex'] = getRandomVelocity() - 1
    sr['movey'] = getRandomVelocity() + 3
    if sr['movex'] < 0:
        sr['surface'] = pygame.transform.scale(L_STINGRAY_IMG, (sr['width'], sr['height']))
    else:
        sr['surface'] = pygame.transform.scale(R_STINGRAY_IMG, (sr['width'], sr['height']))
    sr['bounce'] = 0
    sr['bouncerate'] = random.randint(20, 40)
    sr['bounceheight'] = random.randint(10, 40)
    return sr


def makeNewTurtle(camerax, cameray):
    tt = {}
    generalSize = random.randint(10, 30)
    multiplier = random.randint(2, 3)
    tt['width']  = (generalSize + random.randint(20, 30)) * multiplier
    tt['height'] = (generalSize + random.randint(20, 30)) * multiplier
    tt['x'], tt['y'] = getRandomOffCameraPos(camerax, cameray, tt['width'], tt['height'])
    tt['movex'] = getRandomVelocity() - 3
    tt['movey'] = getRandomVelocity() - 3
    if tt['movex'] < 0:
        tt['surface'] = pygame.transform.scale(L_TURTLE_IMG, (tt['width'], tt['height']))
    else:
        tt['surface'] = pygame.transform.scale(R_TURTLE_IMG, (tt['width'], tt['height']))
    tt['bounce'] = 0
    tt['bouncerate'] = random.randint(20, 40)
    tt['bounceheight'] = random.randint(10, 40)
    return tt


def makeNewCrab(camerax, cameray):
    cr = {}
    generalSize = random.randint(20, 30)
    multiplier = random.randint(1, 1)
    cr['width']  = (generalSize + random.randint(0, 20)) * multiplier
    cr['height'] = (generalSize + random.randint(0, 20)) * multiplier
    cr['x'], cr['y'] = getRandomOffCameraPos(camerax, cameray, cr['width'], cr['height'])
    cr['movex'] = getRandomVelocity() + 2
    cr['movey'] = getRandomVelocity()
    if cr['movex'] < 0:
        cr['surface'] = pygame.transform.scale(L_CRAB_IMG, (cr['width'], cr['height']))
    else:
        cr['surface'] = pygame.transform.scale(R_CRAB_IMG, (cr['width'], cr['height']))
    cr['bounce'] = 0
    cr['bouncerate'] = random.randint(20, 40)
    cr['bounceheight'] = random.randint(10, 30)
    return cr


def makeNewWhale(camerax, cameray):
    wh = {}
    generalSize = random.randint(40, 60)
    multiplier = random.randint(3, 3)
    wh['width']  = (generalSize + random.randint(30, 40)) * multiplier
    wh['height'] = (generalSize + random.randint(30, 40)) * multiplier
    wh['x'], wh['y'] = getRandomOffCameraPos(camerax, cameray, wh['width'], wh['height'])
    wh['movex'] = getRandomVelocity() - 2
    wh['movey'] = getRandomVelocity() - 3
    if wh['movex'] < 0:
        wh['surface'] = pygame.transform.scale(L_KWHALE_IMG, (wh['width'], wh['height']))
    else:
        wh['surface'] = pygame.transform.scale(R_KWHALE_IMG, (wh['width'], wh['height']))
    wh['bounce'] = 0
    wh['bouncerate'] = random.randint(40, 50)
    wh['bounceheight'] = random.randint(10, 20)
    return wh


def makeNewNemo(camerax, cameray):
    nm = {}
    generalSize = random.randint(20, 30)
    multiplier = random.randint(1, 1)
    nm['width']  = (generalSize + random.randint(0, 20)) * multiplier
    nm['height'] = (generalSize + random.randint(0, 20)) * multiplier
    nm['x'], nm['y'] = getRandomOffCameraPos(camerax, cameray, nm['width'], nm['height'])
    nm['movex'] = getRandomVelocity() + 8
    nm['movey'] = getRandomVelocity() + 2
    if nm['movex'] < 0:
        nm['surface'] = pygame.transform.scale(L_NEMO_IMG, (nm['width'], nm['height']))
    else:
        nm['surface'] = pygame.transform.scale(R_NEMO_IMG, (nm['width'], nm['height']))
    nm['bounce'] = 0
    nm['bouncerate'] = random.randint(20, 40)
    nm['bounceheight'] = random.randint(10, 40)
    return nm


def makeNewSquid(camerax, cameray):
    sq = {}
    generalSize = random.randint(20, 30)
    multiplier = random.randint(1, 3)
    sq['width']  = (generalSize + random.randint(10, 20)) * multiplier
    sq['height'] = (generalSize + random.randint(10, 20)) * multiplier
    sq['x'], sq['y'] = getRandomOffCameraPos(camerax, cameray, sq['width'], sq['height'])
    sq['movex'] = getRandomVelocity() - 1
    sq['movey'] = getRandomVelocity() - 1
    if sq['movex'] < 0:
        sq['surface'] = pygame.transform.scale(L_SQUID_IMG, (sq['width'], sq['height']))
    else:
        sq['surface'] = pygame.transform.scale(R_SQUID_IMG, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bouncerate'] = random.randint(30, 50)
    sq['bounceheight'] = random.randint(80, 100)
    return sq


def makeNewReef(camerax, cameray):
    gr = {}
    gr['reefImage'] = random.randint(0, len(REEFIMAGES) - 1)
    gr['width']  = REEFIMAGES[0].get_width()
    gr['height'] = REEFIMAGES[0].get_height()
    gr['x'], gr['y'] = getRandomOffCameraPos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect( (gr['x'], gr['y'], gr['width'], gr['height']) )
    return gr


def isOutsideActiveArea(camerax, cameray, obj):
    # Return False if camerax and cameray are more than
    # a half-window length beyond the edge of the window.
    boundsLeftEdge = camerax - WINWIDTH
    boundsTopEdge = cameray - WINHEIGHT
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, WINWIDTH * 3, WINHEIGHT * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not boundsRect.colliderect(objRect)


def wait_for_key():
    waiting = True
    while waiting:
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False


def draw_text(text, size, color, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    DISPLAYSURF.blit(text_surface, text_rect)


if __name__ == '__main__':
    main()