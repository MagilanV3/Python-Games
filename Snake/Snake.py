# Import necessary modules along with Shorcut 
import pygame as pg
import random as rd
import sys
from pygame.math import Vector2 as V2

#Intialize a class for functions relating to the "snake" object
class Snake:
    
    #Establish the intial co-ordinates
    def __init__(self):
        self.body = [V2(5,10), V2(4,10), V2(3,10)]
        self.direction = V2(1,0)
        self.new_part = False
    
    # Function to draw the snake in the game
    def display_snake(self):
        for part in self.body:
            part_rect = pg.Rect(part.x * cell_s,part.y * cell_s,cell_s,cell_s)
            pg.draw.rect(screen,(23,102,125), part_rect)
    
    # Function for the snake movement
    def snake_movement(self):
        # Condition to allow a new part to be added to the snake 
        if self.new_part == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_part = False
        # Or, show the snake as is, moving
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    # Function to trigger a new part to be added to the snake
    def add_part(self):
        self.new_part = True

#Intialize a class for functions relating to the "Fruit" object
class Fruit:
    
    #Establish the intial co-ordinates
    def __init__(self):
        self.randomize()

    # Function to draw the fruit in the game
    def display_fruit(self):
        fruit_rect = pg.Rect(self.p.x * cell_s,self.p.y * cell_s,cell_s,cell_s)
        screen.blit(apple,fruit_rect)

    # Function to randomize the position of the fruit each time
    def randomize(self):
        self.x = rd.randint(0,cell_n - 1)
        self.y = rd.randint(0,cell_n - 1)
        self.p = V2(self.x, self.y)

#Intialize a class for functions relating to the
class Main:
    
    #Establish the classes
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    #What functions to constantly run 
    def update(self):
        self.snake.snake_movement()
        self.check_collision()
        self.check_fail()
    
    #Function to display score
    def display_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render("Score:" + score_text,True, (56,74,12))
        score_rect = score_surface.get_rect(center = (int(60),int(40)))
        screen.blit(score_surface,score_rect)

    #Function to display the fruit, snake, & score
    def display_elements(self):
        self.fruit.display_fruit()
        self.snake.display_snake()
        self.display_score()
    
    #Function to add a part to the snake when the snake's head touchs the fruit
    def check_collision(self):
        if self.fruit.p == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_part()
        for part in self.snake.body[1:]:
            if part == self.fruit.p:
                self.fruit.randomize()
    
    #Function to end the game if the snake's head hits the body or reachs the boundry
    def check_fail(self):
        
        # Condition to end the game when the snake head hits the boundry of the game
        if not 0 <= self.snake.body[0].x < cell_n or not 0 <= self.snake.body[0].y < cell_n:
            self.game_over()
        
        #Condition to end the game when the snake's head hits the body
        for part in self.snake.body[1:]:
            if part == self.snake.body[0]:
                self.game_over()

    # What happens when "game-ending" actions occur
    def game_over(self):
        pg.quit()
        sys.exit()

# Initiate pygame
pg.init()

#Establish Cell Size & Number to create a display
cell_s = 40
cell_n = 20
display_v = (cell_s * cell_n)
screen = pg.display.set_mode((display_v,display_v))

#Import and establish the icon and name of window
pg.display.set_caption('Snake')
icon = pg.image.load('Snake/Assets/icon.png')
pg.display.set_icon(icon)

# Establish a Timer
clock = pg.time.Clock()

#Import Images & font for the objects in the game
apple = pg.image.load('Snake/Assets/apple.png').convert_alpha()
background = pg.image.load("Snake/Assets/background.png")
game_font = pg.font.Font('freesansbold.ttf', 28)

#Trigger the timer of 150ms when the game starts
screen_update = pg.USEREVENT
pg.time.set_timer(screen_update,150)

main_game = Main()

#The code that runs when the game is running 
while True:
    
    #Set a background
    screen.blit(background,(0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            main_game.game_over()
        if event.type == screen_update:
            main_game.update()
       
        #What each keystroke does
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                #Condition to ensure that the snake object doesn't change direction to go into itself
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = V2(0,-1)
            if event.key == pg.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = V2(0,1)
            if event.key == pg.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = V2(-1,0)
            if event.key == pg.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = V2(1,0)


    #Display the elements
    main_game.display_elements()
    
    #Display the most current objects & values
    pg.display.update()
    clock.tick(60)