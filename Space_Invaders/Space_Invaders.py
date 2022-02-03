# Importing Libraries that are being used
import pygame as pg
import random as rd
import numpy as np

#initialize of pygame
pg.init()

#Set the Display pixel resolution
screen = pg.display.set_mode((800, 600))

#Import & Set the Name and Icon of the display window
pg.display.set_caption("Space Invaders")
icon = pg.image.load('./Space_Invaders/Assets/icon.png')
pg.display.set_icon(icon)

# Import the Background Image
background = pg.image.load("./Space_Invaders/Assets/Background.png")

#Import and Set the Starting position of the Player ship
PlayerImg = pg.image.load('./Space_Invaders/Assets/space.png')
PlayerX = 365
PlayerY = 480
PlayerX_change = 0

#Label the variables used for the Aliens
AlienImg = []
AlienX = []
AlienY = []
AlienX_change = []
AlienY_change = []
number_of_Aliens = 6

#Set the vaiables for the aliens to the intial values
for i in range(number_of_Aliens):
    AlienImg.append(pg.image.load('./Space_Invaders/Assets/Alien.png'))
    AlienX.append(rd.randint(0,736))
    AlienY.append(rd.randint(50,150))
    AlienX_change.append(4)
    AlienY_change.append(40)

#Import and Set the Intial values of the laser
LaserImg = pg.image.load('./Space_Invaders/Assets/Laser.png')
LaserX = 0
LaserY = 480
LaserY_change = 6
Laser_state = "ready"

#Intial Score, font, posistion
score_number = 0
score_font = pg.font.Font('freesansbold.ttf', 34)
textX = 10
textY = 10

#GameOver font
game_over_font = pg.font.Font('freesansbold.ttf', 80)

#Function to display Score
def score_display(x,y):
    score = score_font.render("Score:" + str(score_number), True, (255,255,255))
    screen.blit(score, (x,y))

#Function to display game-over message
def game_over():
    game_over = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over, (200,250))

#Function for the posistion that the player ship is displayed
def player(x,y):
    screen.blit(PlayerImg, (x, y))

#Function for the posistion that the Aliens is displayed
def alien(x,y, i):
    screen.blit(AlienImg[i], (x, y))

#Function for the posistion that the laser is displayed
def shoot_laser (x,y):
    global Laser_state
    Laser_state = "shoot"
    screen.blit(LaserImg, (x+  16, y + 10))

#Function to calculate if the lasers hit the Aliens
def Collision(AlienX, AlienY, LaserX, LaserY) :
    distance = np.sqrt(((LaserX - AlienX)**2)+((LaserY - AlienY)**2))
    if distance < 27:
        return True
    else:
        return False

#Intialize the loop when running the game
running = True
while running:
    #Set the background of the game
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #Defining what each Keystoke does (UP & DOWn arrow key & Spacebar)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                PlayerX_change = -3
            if event.key == pg.K_RIGHT:
                PlayerX_change = 3
            if event.key == pg.K_SPACE:
                LaserX = PlayerX
                shoot_laser(LaserX, LaserY)
        #Defining when no keys are pressed
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                PlayerX_change = 0
    
    #Player ship Boundry
    PlayerX += PlayerX_change
    if PlayerX <=0:
        PlayerX = 0
    elif PlayerX >= 737:
        PlayerX = 737
    
    #When the Aliens reach the player ship, the game ends
    for i in range(number_of_Aliens):
        if AlienY[i] > 440:
            for j in range(number_of_Aliens):
                AlienY[j] = 2000
            game_over()
            break
        # Alien boundry
        AlienX[i] += AlienX_change[i]
        if AlienX[i] <=0:
            AlienX_change[i] = 1
            AlienY[i] += AlienY_change[i]
        elif AlienX[i] >= 737:
            AlienX_change[i] = -1
            AlienY[i] += AlienY_change[i]
       # If the lasers hit the aliens, the aliens respawn
        collision = Collision(AlienX[i], AlienY[i], LaserX, LaserY)
        if collision:
            LaserY = 480
            Laser_state = "ready"
            score_number += 1
            AlienX[i] = rd.randint(0,736)
            AlienY[i] = rd.randint(50,150)
            
        alien(AlienX[i], AlienY[i], i)

# Laser boundries and Reload
    if LaserY <= 0:
        LaserY = 480    
        Laser_state = "ready"
    if Laser_state == "shoot":
        shoot_laser(LaserX, LaserY)
        LaserY -= LaserY_change

    
    # Moving Player ship
    player(PlayerX, PlayerY)
    # Display the current score
    score_display(textX, textY)
    # Display using the current values
    pg.display.update()