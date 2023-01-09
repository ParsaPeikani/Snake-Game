###################################################################################Imports &Constants#############################################################################################
from turtle import Turtle
from venv import create
from pygame import mixer
import pygame
import sys
from pygame.locals import *
import time
import random
import os

# Creating different colors of the Rectangels
light_green = (227,207,87)
dark_green = (107,142,35)
darker_green = (0,100,0)

# The amount by which the snake move to each direction
SIZE = 32
counting = False
##################################################################################################################################################################################################

# General setup
pygame.init()
bg = pygame.image.load("background.jpg")
clock = pygame.time.Clock()

# Creating a class for the snake
class Snake():
    # laoding the block on the screen and giving length as an atribute
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("snake.png")
        self.image_square = pygame.image.load("square.png")
        self.direction = 'down'
        self.reversed_movement = False
        # Starting length for the snake
        self.length = length

        self.SIZE = 32

        # Positions of the snake blocks, we multiply it by the length so it create a list for all the snake blocks positions we want
        self.x = [392] * (length+1)
        self.y = [316] * (length+1)

        # Starting the counter from 0
        self.counter = 0

        # Making a variable to use when eating the slowDeath potion
        self.slowdeath = False

        # Making a variable to use when eating the Translucent potion
        self.translucent = False

    # Creating function for the snake moving left
    def move_left(self):
        self.direction = 'left'

    # Creating function for the snake moving right
    def move_right(self):
        self.direction = 'right'

    # Creating function for the snake moving up
    def move_up(self):
        self.direction = 'up'

    # Creating function for the snake moving down
    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update each block of the snake, making them go where ever the first block goes
        for i in range(self.length, 0,-1):
            self.x[i] = self.x[i-1] 
            self.y[i] = self.y[i-1] 

        # update the position of the first block based on the direction
        if self.direction == 'left':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.x[0] -= self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'right':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.x[0] += self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'up':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.y[0] -= self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'down':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.y[0] += self.SIZE
            self.draw()

        self.restore_background(self.square_x, self.square_y)

    def restore_background(self, square_x, square_y):

        # crop the background in the desired coordinates and put it back in place of the removed object
        self.parent_screen.blit(bg, (square_x, square_y), (square_x, square_y-120, self.SIZE, self.SIZE))
        pygame.display.flip()

    # Creating different blocks of the snake at the beginning of the game
    def draw(self):
        # for i in range(self.length):
        self.parent_screen.blit(self.image, (self.x[0], self.y[0]))

        pygame.display.flip()

    def draw_square(self):
        self.parent_screen.blit(self.image_square, (self.square_x, self.square_y))
        pygame.display.flip()

    # Creating a function for increasing the length each time the snake eats an apple
    def increase_length(self):

        # We have to increase the length
        self.length += 1

        # We can put any value inside the bracket because it will update automatically
        self.x.append(-1)
        self.y.append(-1)

    # Creating a function for decreasing the length each time the snake eats a poison
    def decrease_length(self):

        # We have to decrease the length by one factor
        self.length -= 1
        self.restore_background(self.x[-2], self.y[-2])
        # We have to pop the last block of the snake so we put -1
        self.x.pop(-1)
        self.y.pop(-1)

    # Creating a function to count the number of apples eaten by the snake
    def counting(self):
        self.counter += 1

# Creating a class for the snake
class Opponenet():
    # laoding the block on the screen and giving length as an atribute
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("opponent.png")
        self.direction = 'up'

        # Starting length for the snake
        self.length = length

        self.SIZE = 32

        # Positions of the snake blocks, we multiply it by the length so it create a list for all the snake blocks positions we want
        self.x = [72] * (length+1)
        self.y = [316] * (length+1)

        # Starting the counter from 0
        self.counter = 0

    # Creating function for the snake moving left
    def move_left(self):
        self.direction = 'left'

    # Creating function for the snake moving right
    def move_right(self):
        self.direction = 'right'

    # Creating function for the snake moving up
    def move_up(self):
        self.direction = 'up'

    # Creating function for the snake moving down
    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update each block of the snake, making them go where ever the first block goes
        for i in range(self.length, 0,-1):
            self.x[i] = self.x[i-1] 
            self.y[i] = self.y[i-1] 

        # update the position of the first block based on the direction
        if self.direction == 'left':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.x[0] -= self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'right':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.x[0] += self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'up':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.y[0] -= self.SIZE
            self.draw()

            # self.draw_square()
        if self.direction == 'down':
            self.square_x = self.x[-1]
            self.square_y = self.y[-1]
            self.y[0] += self.SIZE
            self.draw()

        self.restore_background(self.square_x, self.square_y)

    def restore_background(self, square_x, square_y):

        # crop the background in the desired coordinates and put it back in place of the removed object
        self.parent_screen.blit(bg, (square_x, square_y), (square_x, square_y-120, self.SIZE, self.SIZE))
        pygame.display.flip()

    # Creating different blocks of the snake at the beginning of the game
    def draw(self):
        # for i in range(self.length):
        self.parent_screen.blit(self.image, (self.x[0], self.y[0]))

        pygame.display.flip()


# Creating a class for the object apple
class Apple():
    # Setting the screen for apple and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png")
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.set_apple_x =  [104]
        self.set_apple_y = [348]

    # Creating a function to draw the apple object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Creating a function to move the apple randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

# Creating a class for the Game
class Game():
    def __init__(self):
        pygame.init()

        # setting up the caption of the game
        pygame.display.set_caption("Snake Game")

        # if there is no score.txt file, it will be created
        if os.path.exists('score.txt'):

            # We will use the high_score stored in the txt file to show the highscore
            with open('score.txt', 'r')  as  file:
                self.high_score = int(file.read())
        else:
            self.high_score = 0

        # Setting a variable for the speed of the snake
        self.speed = 10000

        # Setting a variable for the speed of the snake
        self.opponent_speed = 0

        # Creating a variable for the block object, make it true when snake has passed through it when eaten the translucent potion
        self.translucent = False

        self.collision = False

        # Creating the varibales for creting timer
        self.current_time = 0
        self.button_press = 0

        # To avoid drawing objects multiple times
        self.rendered = False

        # Setting up the main window
        self.surface  = pygame.display.set_mode((1200, 960))
        self.surface.fill((255, 255, 255))
        #pygame.display.update()
        
        # Setting the background music and the sounds
        pygame.mixer.init()

        # self.play_background_music()

        # Creating a varibale for the length of the snake 
        self.default_length = 3

        # Creating a variable for the length of the snake's opponent
        self.default_length_opponent = 10

        # Creating a class snake and drawing it
        #self.snake = Snake(self.surface, self.default_length)
        #self.snake.draw()

        self.opponent = Opponenet(self.surface, self.default_length_opponent)
        self.opponent.draw()

        # Creating a class apple and drawing it
        self.apple = Apple(self.surface)
        self.apple.draw()

    # Creating a function to play the background music
    def play_background_music(self):
        pygame.mixer.music.load('MP3.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0)

    # Creating a function to play the different sound effects 
    def play_sound(self, sound_name):
        if sound_name == "game over":
            sound = pygame.mixer.Sound("game over.mp3")

        elif sound_name == 'eating':
            sound = pygame.mixer.Sound("eating.mp3")

        elif sound_name == "woosh":
            sound = pygame.mixer.Sound("woosh.mp3")

        elif sound_name == "slow":
            sound = pygame.mixer.Sound("slow.mp3")

        elif sound_name == "vomit":
            sound = pygame.mixer.Sound("vomit.mp3")

        elif sound_name == "crash":
            sound = pygame.mixer.Sound("crash.mp3")

        elif sound_name == "dizzy":
            sound = pygame.mixer.Sound("dizzy.mp3")

        elif sound_name == "slow_death":
            sound = pygame.mixer.Sound("slow_death.mp3")

        pygame.mixer.Sound.play(sound)

    # We must create boundaries for the snake to stay in the green zone
    def boundaries(self, x1, y1):
        if (x1 < 40) or (x1 > 1159) or (y1 < 155) or (y1 > 923):
            return True
        return False
    
    # We must create boundaries for the opponenet to stay in the green zone
    def opponent_boundaries(self, x1, y1):
        if (x1 < 72) or (x1 > 1127) or (y1 < 172) or (y1 > 891):
            return True
        return False

    # Creating the reset function when the player presses the enter button   
    def reset(self):
        self.render_background()
        self.speed = 10
        self.opponent_speed = 10
        self.snake = Snake(self.surface, self.default_length)
        self.apple = Apple(self.surface)

    # Creating a function when there is a collision happening between the snake and other objects
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
        
    def play(self):

        # Creating the background, visuals, and the objects on the screen

        if not self.rendered:
            self.render_background()
            self.game_visuals()
            self.apple.draw()
            pygame.display.flip()
            self.rendered = True

        if self.rendered:
            self.opponent.walk()
            pygame.display.flip()

################################################################# ALL THE CONDITIONS FOR THE DIFFERENT COLLISIONS ##################################################################################



        # Opponent hitting the boundaries of the game(4 different sides)
        if self.opponent_boundaries(self.opponent.x[0], self.opponent.y[0]) == True:
            if (self.opponent.direction == 'right') and (self.opponent.x[0] > 1127):
                self.opponent.direction = 'down'
            elif (self.opponent.direction == 'left') and (self.opponent.x[0] < 72):
                self.opponent.direction = 'up'
            elif (self.opponent.direction == 'up') and (self.opponent.y[0] < 172):
                self.opponent.direction = 'right'
            elif (self.opponent.direction == 'down') and (self.opponent.y[0] > 891):
                self.opponent.direction = 'left'

        



        

###################################################################################################################################################################################################
    # for displaying the score of the player
    def display_score(self):
        font = pygame.font.SysFont('arial',70)

        # We use the counter to display the score of the player
        score = font.render(f"Score:   ",True,(0,0,0))
        self.surface.blit(score,(20,10))

        pygame.display.flip()
            
    # saving the highest score when the game is over
    def saving_high_score(self):

        # if the snake counter gets higher than the high_score, then they would be equal:
        if self.snake.counter >= self.high_score:

            # We set the high_score equal to the snake counter
            self.high_score = self.snake.counter

            # We overwrite the previous highscore with the new one
            with open('score.txt', 'w') as file:
                file.write(str(self.high_score))

    # VISUALS

    # making the highest score
    def display_hihgest_score(self):
        font = pygame.font.SysFont('arial',70)

        # We use the counter to display the score of the player
        score = font.render(f"Highest Score: {self.high_score}",True,(0,0,0))
        self.surface.blit(score,(740,10))

        pygame.display.flip()

    # making visuals of the game infor screen 
    def load_game_info_screen(self):
        
        self.info_screen = pygame.Rect( 0, 0, 1200, 120)
        pygame.draw.rect(self.surface, light_green, self.info_screen)
        pygame.display.flip()

        # for displaying the score of the player and the images
        self.display_score()
        self.load_info_images()
        self.display_hihgest_score()

    # Creating a function to display the image of apple and block
    def load_info_images(self): 

        # For the apple image
        image_1 = pygame.image.load("apple_menu.png")
        self.surface.blit(image_1, (270, 21))

        pygame.display.flip()

    # making visuals of the game
    def game_visuals(self):
        self.left_side = pygame.Rect( 0, 156, 40, 768)
        pygame.draw.rect(self.surface, dark_green, self.left_side)

        self.up_side = pygame.Rect( 0, 120, 1200, 36)
        pygame.draw.rect(self.surface, dark_green, self.up_side)

        self.right_side = pygame.Rect(1160 , 156, 40, 768)
        pygame.draw.rect(self.surface, dark_green, self.right_side)

        self.down_side = pygame.Rect( 0, 924, 1200, 36)
        pygame.draw.rect(self.surface, dark_green, self.down_side)
        pygame.display.flip()

    # Choosing the background image
    def render_background(self):

        self.surface.blit(bg, (0,120))

    # Choosing the background image when is game over
    def render_gameover_background(self):
        bg = pygame.image.load("gameover.jpg")
        self.surface.blit(bg, (-1320,-620))

    # Visuals for the game over screen
    def show_game_over(self):

        # updating highest score
        self.saving_high_score()

        self.render_gameover_background()
        font1 = pygame.font.SysFont('arial', 100)
        line1 = font1.render(f"Game is over!", True, (255, 68, 51))
        self.surface.blit(line1, (640, 60))
        font2 = pygame.font.SysFont('arial', 65)
        line2 = font2.render(f"Your score is {self.snake.counter}", True, (255, 68, 51))
        self.surface.blit(line2, (588, 328))
        font3 = pygame.font.SysFont('arial', 60)
        line3 = font3.render("To play again press Enter", True, (255, 68, 51))
        self.surface.blit(line3, (300, 730))
        line4 = font3.render("To exit press Escape", True, (255, 68, 51))
        self.surface.blit(line4, (350, 825))
        pygame.mixer.music.pause()

        pygame.display.flip()

    def run(self):

        running = True
        pause = False

        # We want the info screen reload once
        self.load_game_info_screen()
        self.render_background()
        #frameRate = self.speed
        while running:
            
            frameRate = self.speed

            for event in pygame.event.get():
                # We have to check if any key is pressed first
                if event.type == KEYDOWN:

                    # making the game QUIT if the escape button is pressed
                    if event.key == K_ESCAPE:

                        # updating highest score
                        self.saving_high_score()
                        
                        running = False

                    # Making the game to reload again if enter is pressed
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.load_game_info_screen()
                        self.game_visuals()
                        self.snake.walk()
                        self.apple.draw()
                        pygame.display.flip()

                    # We make the different moves based on the key pressed if pause is True
                    if not pause:
                        if ((not self.snake.reversed_movement) and event.key == K_LEFT) :
                            if not (self.snake.x[1] < self.snake.x[0]):
                                self.snake.move_left()

                        elif ((not self.snake.reversed_movement) and event.key == K_RIGHT):
                            if not (self.snake.x[1] > self.snake.x[0]):
                                self.snake.move_right()

                        elif ((not self.snake.reversed_movement) and event.key == K_UP):
                            if not (self.snake.y[1] < self.snake.y[0]):
                                self.snake.move_up()

                        elif ((not self.snake.reversed_movement) and event.key == K_DOWN):
                            if not (self.snake.y[1] > self.snake.y[0]):
                                self.snake.move_down()

                # Making the game QUIT if the cross is pressed
                elif event.type  == pygame.QUIT:

                    # updating highest score
                    self.saving_high_score()
                    
                    running = False
            self.current_time = pygame.time.get_ticks()

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                print(e)
                pause = True
                self.reset()
                        
            # Updaiting the wondow
            clock.tick(frameRate)

if __name__ == '__main__':
    game = Game()
    game.run()

# Make the translucent potion 
# Make it so that potions don't spawn on each other
# Make the buttons better on the menu page
# Give the user the option to click the objects and customize it for the game
# Put the reverse and other objects on top of othe screen and make them so that they fade
# Make the escape option during the game
# Change the information screen of the main page