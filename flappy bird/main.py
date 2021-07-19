import random  #for generating random pipes
import sys     #for exit
import pygame
from pygame.locals import *  #basic pygame imports

#Global variable
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    """
    shows welcome image on the screen
    """

    playerx = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            #exit if cross button is clicked
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if user presses space or up key start the game
            elif (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) :
                return
            
            else:
                #blitting - pasting image on screen
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def choose_level():
    while True:
        for event in pygame.event.get():
            #exit if cross button is clicked
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # # if user presses space or up key start the game
            # elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            #     return

            elif event.type == MOUSEBUTTONDOWN :
                """
                parameters : horizontal_dis, offset, pipeVelx, pipe_add_dis(distance at which new
                pipe is added when the leftmost pipe is at distance x)
                """
                if 0 < pygame.mouse.get_pos()[1] < SCREENHEIGHT/3:
                    print(f"Level : hard")
                    return {'horizontal_dis' : 10*2, 'offset' : SCREENHEIGHT/5, 'pipeVelx' : -5, 'pipe_add_dis' : 5 }
                elif SCREENHEIGHT/3 < pygame.mouse.get_pos()[1] < (2/3)*SCREENHEIGHT:
                    print(f"Level : medium")
                    return {'horizontal_dis' : 15*2, 'offset' : SCREENHEIGHT/4, 'pipeVelx' : -4, 'pipe_add_dis' : 4 }
                else:
                    print(f"Level : easy")
                    return {'horizontal_dis' : 20*2, 'offset' : SCREENHEIGHT/3, 'pipeVelx' : -3, 'pipe_add_dis' : 3 }

            #parameters for level - 1.horizontal distance b/w pipe  2. offset- vertical distance b/w pipes 3.pipe velocity

            
            
            else:
                #blitting - pasting image on screen
                SCREEN.blit(GAME_SPRITES['level'],(0,0))            
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame( level ):
    
    score = 0 
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    #create two pipes for bliting on screen
    newpipe1 = getRandomPipe(level)
    newpipe2 = getRandomPipe(level)

    #list of upper pipes 
    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newpipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : newpipe2[0]['y']},
        
    ]

    #list of lower pipes
    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newpipe1[1]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : newpipe2[1]['y']},
        
    ]

    # print(f"wtf {upperPipes}")

    pipeVelX = level['pipeVelx']
    playerVelY = -9
    playerMinVelY = -8
    playerMaxVelY = 10
    playerAccY = 1

    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False # true only when bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0 :
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            return

        #cheking for score
        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < (pipeMidPos + 4):
                score += 1 
                print(f"Your score is {score}")   
                GAME_SOUNDS['point'].play()
        
        

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipes to left
     
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

    
        # Add a new pipe when the first is about to cross the leftmost part of the screen
      
        if 0< upperPipes[0]['x'] < level['pipe_add_dis']:
            newpipe = getRandomPipe(level)
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


          # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        

        #blitng (pasting) the sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

       
        
        myDigits = [int(x) for x in list(str(score))]
        width = 0 
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 5:  #height of player is almost 25
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()- 18):     #18 is adjusted value (hit and try)
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < (GAME_SPRITES['pipe'][0].get_width()-18):
            GAME_SOUNDS['hit'].play()
            return True


    return False

def getRandomPipe(level):
    """
    generation position of two vertically opposite pipes
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = level['offset']  # space b/w two veritcally opposite pipes
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + level['horizontal_dis']
    y1 = pipeHeight -y2 + offset
    pipe = [                                       
        {'x' : pipeX, 'y' : -y1 },
        {'x' : pipeX, 'y' : y2}
    ]
    return pipe

if __name__ == "__main__":
    #starting point of the game
    pygame.init()  #initialize all pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy bird game")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),        
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['level'] = pygame.image.load('gallery/sprites/level.png')

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:        
        welcomeScreen()   #welcome screen until game starts
        level = choose_level()    #choosing level(easy, medium, hard)
        mainGame(level)          # main game of program