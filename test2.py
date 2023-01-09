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
import numpy as np

# Creating different colors of the Rectangels
light_green = (227, 207, 87)
dark_green = (107, 142, 35)
darker_green = (0, 100, 0)

# The amount by which the snake move to each direction
width = 1200
height = 960
SIZE = 32
board_y_offset = 120
border_height = 36
game_y_offset = board_y_offset + border_height
board_x_offset = 0
border_width = 40
game_x_offset = board_x_offset + border_width
counting = False

##################################################################################################################################################################################################
grid = np.zeros((25, 36), dtype=int)  # grid is one square larger than actual game size


def translate_to_grid(x, y):
    if x >= width or y >= height:
        return (24, 35)
    return (y - game_y_offset) // SIZE, (x - game_x_offset) // SIZE


def translate_to_coords(y, x):
    return x * SIZE + game_x_offset, y * SIZE + game_y_offset


##################################################################################################################################################################################################

# General setup
pygame.init()
bg = pygame.image.load("background.jpg")
clock = pygame.time.Clock()


# Creating a class for the snake
class Snake():  # object ID: 1
    # laoding the block on the screen and giving length as an atribute
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("snake.png")
        self.image_square = pygame.image.load("square.png")
        self.direction = 'down'
        self.reversed_movement = False
        # Starting length for the snake
        self.length = length
        self.background_just_restored = (-1, -1)
        self.SIZE = 32

        # Positions of the snake blocks, we multiply it by the length so it create a list for all the snake blocks positions we want
        self.x = [72] * (length + 1)
        self.y = [316] * (length + 1)

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
        for i in range(self.length, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

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
        self.parent_screen.blit(bg, (square_x, square_y),
                                (square_x - board_x_offset, square_y - board_y_offset, self.SIZE, self.SIZE))
        self.background_just_restored = (square_x, square_y)
        y1, x1 = translate_to_grid(square_x, square_y)
        grid[y1, x1] = 0

        pygame.display.flip()

    # Creating different blocks of the snake at the beginning of the game
    def draw(self):
        # for i in range(self.length):
        self.parent_screen.blit(self.image, (self.x[0], self.y[0]))
        y1, x1 = translate_to_grid(self.x[0], self.y[0])
        grid[y1, x1] = 1
        # optimize to track a snippet around the snake's head (incomplete)
        # for y in grid[min(y1 - 2, 0):max(y1 + 3, 24)]:
        #     for x in grid[min(x1 - 2, 0):max(x1 + 3, 35)]:
        #         if grid[y, x] == 0:
        #             grid[y, x] = 1

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


# Creating a class for the object apple
class Apple():  # object ID: 3
    # Setting the screen for apple and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png")
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.set_apple_x = [104]
        self.set_apple_y = [348]

    # Creating a function to draw the apple object
    def draw(self):
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 3
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break

        pygame.display.flip()

    # Creating a function to move the apple randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()


# Creating a class for the object rottenapple
class RottenApple:  # object ID: 4
    # Setting the screen for rottenapple and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("rotten_apple.png")
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.set_poison_x = [136]
        self.set_poison_y = [380]

    # drawing the poison object
    def draw(self):
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 4
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the poison randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()


# Creating a class for the object block
class Block():  # object ID: 2
    # Setting the screen for apple and creating its positions
    def __init__(self, parent_screen, number):
        self.parent_screen = parent_screen
        self.number = number
        self.image = pygame.image.load("block.png")
        # self.image_2 = pygame.image.load()
        self.x = [random.randint(1, 35) * SIZE + 8]
        self.y = [random.randint(4, 27) * SIZE + 28]

    # Creating a function to draw the block object
    def draw(self, index=None):
        # Creating a for loop to draw every block that's been created
        if index is None:
            index = len(self.x)-1
            # # fix this portion to account for collisions
            # while True:
            #     for i in range(self.number):
            #         if self.x[i] <= width and self.y[i] <= height:
            #             y, x = translate_to_grid(self.x[i], self.y[i])
            #             if grid[y, x] == 0:
            #                 self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            #                 grid[y, x] = 2
            #                 break
            #             else:
            #                 self.x[i] = random.randint(1, 35) * SIZE + 8
            #                 self.y[i] = random.randint(4, 27) * SIZE + 28
            #         else:
            #             break
            #     break
        while True:

            if self.x[index] <= width and self.y[index] <= height:
                y, x = translate_to_grid(self.x[index], self.y[index])
                if grid[y, x] == 0:
                    grid[y, x] = 2
                    self.parent_screen.blit(self.image, (self.x[index], self.y[index]))
                    break
                self.x[index] = random.randint(1, 35) * SIZE + 8
                self.y[index] = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a funciton to draw the block object with more transparency
    def draw_2(self, index=None):
        # do not set block ID for this
        # Drawing only a certain block
        self.parent_screen.blit(self.image_2, (self.x[index], self.y[index]))
        pygame.display.flip()

    # Creating new Blocks
    def new_blocks(self):
        # We want the number of blocks increase every time we eat an apple
        self.number += 1

        # We can append a random location to the list of positions
        self.x.append(random.randint(1, 35) * SIZE + 8)
        self.y.append(random.randint(4, 27) * SIZE + 28)
        self.draw()


# Creating a class for the potion object
class SpeedPotion:  # object ID: 5
    # Setting the screen for potion and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("potion.png")
        # We put large position so they don't appear on the screen
        self.x = 20000
        self.y = 44400

    # Creating a function to draw the poition object
    def draw(self):
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 5
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the potion randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

    # Creating a function to move the potion outside the screen
    def move_outside(self):
        self.x = 2700
        self.y = 2700
        self.draw()


# Creating a class for the object Poision
class Poison:  # object ID: 6
    # Setting the screen for poison and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("poison.png")

        # We put large position so they don't appear on the screen
        self.x = 23200
        self.y = 47600

    # drawing the poison object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 6
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the poison randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

    # Creating a function to move the potion outside the screen
    def move_outside(self):
        self.x = 2700
        self.y = 2700
        self.draw()


class ReversePotion:  # object ID: 7
    # Setting the screen for ReversePotion and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("reverse_potion.png")

        # We put large position so they don't appear on the screen
        self.x = 3000
        self.y = 3000

    # drawing the object
    def draw(self):
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 7
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the potion randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

    # Creating a function to move the potion outside whenever it gets eaten by the snake
    def move_outside(self):
        self.x = 2700
        self.y = 2700
        self.draw()


class SlowDeathPotion:  # object ID: 8
    # Setting the screen for SlowDeathPotion and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("slow_death.png")

        # We put large position so they don't appear on the screen
        self.x = 3100
        self.y = 3100

    # drawing the object
    def draw(self):
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 8
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the potion randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

    # Creating a function to move the potion outside whenever it gets eaten by the snake
    def move_outside(self):
        self.x = 2800
        self.y = 2800
        self.draw()


class TranslucentPotion:  # object ID: 9
    # Setting the screen for TranslucentPotion and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("translucent_potion.png")

        # We put large position so they don't appear on the screen
        self.x = 3200
        self.y = 3200

    # drawing the object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        while True:
            if self.x <= width and self.y <= height:
                y, x = translate_to_grid(self.x, self.y)
                if grid[y, x] == 0:
                    grid[y, x] = 9
                    self.parent_screen.blit(self.image, (self.x, self.y))
                    break
                self.x = random.randint(1, 35) * SIZE + 8
                self.y = random.randint(4, 27) * SIZE + 28
            else:
                break
        pygame.display.flip()

    # Creating a function to move the potion randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28
        self.draw()

    # Creating a function to move the potion outside whenever it gets eaten by the snake
    def move_outside(self):
        self.x = 2700
        self.y = 2700
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
            with open('score.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            self.high_score = 0

        # Setting a variable for the speed of the snake
        self.speed = 10

        # Creating the varibales for creting timer
        self.current_time = 0
        self.button_press = 0

        # To avoid drawing objects multiple times
        self.rendered = False

        # Setting up the main window
        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill((255, 255, 255))
        # pygame.display.update()

        # Setting the background music and the sounds
        pygame.mixer.init()
        # self.play_background_music()
        self.default_length = 30
        # Creating a class snake and drawing it
        self.snake = Snake(self.surface, self.default_length)
        self.snake.draw()

        # Creating a class apple and drawing it
        self.apple = Apple(self.surface)
        self.apple.draw()

        # Creating a class rottenapple and drawing it
        self.rottenapple = RottenApple(self.surface)
        self.rottenapple.draw()

        # Creating a class block and drawing it
        self.block = Block(self.surface, 1)
        self.block.draw()

        # Creating a class for potion and drawing it
        self.speedPotion = SpeedPotion(self.surface)
        self.speedPotion.draw()

        # Creating a class poison and drawing it
        self.poison = Poison(self.surface)
        self.poison.draw()

        # Creating a class ReversePotion and drawing it
        self.reversepotion = ReversePotion(self.surface)
        self.reversepotion.draw()

        # Creating a class SlowDeathPotion and drawing it
        self.SlowDeathPotion = SlowDeathPotion(self.surface)
        self.SlowDeathPotion.draw()

        # Creating a class TranslucentPotion and drawing it
        self.TranslucentPotion = TranslucentPotion(self.surface)
        self.TranslucentPotion.draw()

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
        if (x1 < game_x_offset) or (x1 >= width - border_width) or (y1 < game_y_offset) or (
                y1 >= height - border_height):
            return True
        return False

    # Creating the reset function when the player presses the enter button   
    def reset(self):
        self.render_background()
        self.speed = 10
        self.snake = Snake(self.surface, self.default_length)
        self.apple = Apple(self.surface)
        self.rottenapple = RottenApple(self.surface)
        self.block = Block(self.surface, 1)
        self.speedPotion = SpeedPotion(self.surface)
        self.poison = Poison(self.surface)
        self.reversepotion = ReversePotion(self.surface)
        self.SlowDeathPotion = SlowDeathPotion(self.surface)
        self.TranslucentPotion = TranslucentPotion(self.surface)

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
            self.rottenapple.draw()
            self.block.draw()
            self.speedPotion.draw()
            self.poison.draw()
            self.reversepotion.draw()
            self.SlowDeathPotion.draw()
            self.TranslucentPotion.draw()
            pygame.display.flip()
            self.rendered = True

        if self.rendered:
            self.snake.walk()
            # in case of translucent snake, need to restore the block
            x, y = self.snake.background_just_restored
            for i in range(0, self.block.number):
                if self.is_collision(x, y, self.block.x[i], self.block.y[i]):
                    self.block.draw(i)

            pygame.display.flip()
        ####################################################################### Conditions to first spawn an object########################################################################################

        # We want the potion and the poison to spawn if the score is equal or more than 5
        if self.snake.counter == 5 and self.speedPotion.x > 2800:
            self.speedPotion.move()
            self.poison.move()

        # We want the reversepotion to spawn if the score is equal or more than 10
        if self.snake.counter == 11 and self.reversepotion.x > 2800:
            self.reversepotion.move()

        # We want the SlowDeathPotion to spawn if the score is equal or more than 20
        if self.snake.counter == 1 and self.SlowDeathPotion.x > 2800:
            self.SlowDeathPotion.move()

        # We want the TranslucentPotion to spawn if the score is equal or more than 15
        if self.snake.counter == 2 and self.TranslucentPotion.x > 2800:
            self.TranslucentPotion.move()

        ################################################################# ALL THE CONDITIONS FOR THE DIFFERENT COLLISIONS ##################################################################################

        # Snake eating the poison when has a length of 1, avoiding score of -1 at the beggining
        if self.snake.length <= 2:
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.rottenapple.x, self.rottenapple.y):
                # self.play_sound('game over')
                raise "Collision Occurred"

        # Snake hitting the boundaries of the game(4 different sides)
        if self.boundaries(self.snake.x[0], self.snake.y[0]) == True:
            # self.play_sound('game over')
            raise "Collision Occurred"

        # snake hitting the apple(eating it)
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eating")

            if self.snake.slowdeath == True:
                self.snake.slowdeath = False
                self.SlowDeathPotion.move()

            self.snake.increase_length()
            self.snake.counting()
            self.block.new_blocks()
            self.apple.move()
            self.load_game_info_screen()

            # Updating the highest score if the current score is higher to display on the screen
            if self.high_score < self.snake.counter:
                self.high_score += 1

        # snake eating rottenapple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.rottenapple.x, self.rottenapple.y):
            self.play_sound("vomit")
            self.rottenapple.move()
            self.snake.decrease_length()

        # snake eating potion
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.speedPotion.x, self.speedPotion.y):
            self.play_sound("woosh")

            # Making the snake faster 
            self.speed += 5

            if self.speed > 20:
                self.speedPotion.move_outside()
            else:
                self.speedPotion.move()

            # Moving the poison object to the screen
            if self.poison.x > 2000:
                self.poison.move()

        # We want the poison object to be outside if the speed is 4
        if self.speed < 10:
            self.poison.move_outside()

        # snake eating poison
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.poison.x, self.poison.y):
            self.play_sound("slow")

            # Making the snake slower 
            self.speed -= 5

            if self.speed < 10:
                self.poison.move_outside()

            else:
                # if self.speed >  5:
                self.poison.move()

            if self.speedPotion.x > 2000:
                self.speedPotion.move()

        # snake eating ReversePotion
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.reversepotion.x, self.reversepotion.y):
            self.play_sound("dizzy")

            # We DON'T reverse the value of self.snake.SIZE
            self.button_press = pygame.time.get_ticks()
            self.snake.reversed_movement = True
            self.reversepotion.move_outside()

        # snake eating SlowDeathPotion
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.SlowDeathPotion.x, self.SlowDeathPotion.y):
            self.play_sound("slow_death")
            self.SlowDeathPotion.move_outside()

            # Making the slowdeath variable True
            self.snake.slowdeath = True
            self.button_press_1 = pygame.time.get_ticks()

        # snake eating TranslucentPotion
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.TranslucentPotion.x, self.TranslucentPotion.y):
            self.play_sound("slow_death")
            self.TranslucentPotion.move_outside()

            # Making the Translucent variable True
            self.snake.translucent = True
            self.button_press_2 = pygame.time.get_ticks()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # self.play_sound('game over')
                raise "Collision Occurred"

        # snake hitting the block(eating it)
        for i in range(0, self.block.number):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.block.x[i],
                                 self.block.y[i]) and self.snake.translucent == False:
                self.play_sound('crash')
                # self.play_sound('game over')
                raise "Collision Occurred"

        ################################################################# Different Times for Different Potions###########################################################################################

        # Creating an if statement to move the potion into the screen after a certain time
        if self.snake.reversed_movement and (self.current_time - self.button_press > 5000):
            self.snake.reversed_movement = False
            self.reversepotion.move()

        # Decreasing the length every 0.5 seconds
        if (self.snake.slowdeath == True) and (self.current_time - self.button_press_1 > 1000):
            self.snake.decrease_length()

            # We want the game to be over once the length reaches 0:
            if self.snake.length < 1:
                raise "Collision Occurred"

            self.button_press_1 = pygame.time.get_ticks()

        # Drawing the block so that it doesn't disappear when snake is moving through it
        if self.snake.translucent:
            # passed_blocks = []
            for i in range(0, self.block.number):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.block.x[i],
                                     self.block.y[i]):
                    self.block.draw(i)
                    # passed_blocks.append(i)

        # Creating an if statement to move the potion into the screen after a certain time
        if self.snake.translucent and (self.current_time - self.button_press_2 > 5000):
            self.snake.translucent = False
            self.TranslucentPotion.move()

    ###################################################################################################################################################################################################
    # for displaying the score of the player
    def display_score(self):
        font = pygame.font.SysFont('arial', 70)

        # We use the counter to display the score of the player
        score = font.render(f"Score: {self.snake.counter}", True, (0, 0, 0))
        self.surface.blit(score, (20, 10))

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

    # for displaying the number of blocks on the screen
    def display_number_blocks(self):
        font = pygame.font.SysFont('arial', 70)

        # We use the second counter to display the score of the player
        score = font.render(f"Blocks: {self.block.number}", True, (0, 0, 0))
        self.surface.blit(score, (370, 10))

        pygame.display.flip()

    # VISUALS

    # making the highest score
    def display_hihgest_score(self):
        font = pygame.font.SysFont('arial', 70)

        # We use the counter to display the score of the player
        score = font.render(f"Highest Score: {self.high_score}", True, (0, 0, 0))
        self.surface.blit(score, (740, 10))

        pygame.display.flip()

    # making visuals of the game infor screen 
    def load_game_info_screen(self):

        self.info_screen = pygame.Rect(0, 0, width, board_y_offset)
        pygame.draw.rect(self.surface, light_green, self.info_screen)
        pygame.display.flip()

        # for displaying the score of the player and the images
        self.display_score()
        self.display_number_blocks()
        self.load_info_images()
        self.display_hihgest_score()

    # Creating a function to display the image of apple and block
    def load_info_images(self):

        # For the apple image
        image_1 = pygame.image.load("apple_menu.png")
        self.surface.blit(image_1, (270, 21))

        # For the block image
        image_2 = pygame.image.load("block_menu.png")
        self.surface.blit(image_2, (640, 21))

        pygame.display.flip()

    # making visuals of the game
    def game_visuals(self):
        self.left_side = pygame.Rect(0, board_y_offset + border_height, game_x_offset - board_x_offset,
                                     height - board_y_offset - 2 * border_height)
        pygame.draw.rect(self.surface, dark_green, self.left_side)

        self.up_side = pygame.Rect(0, board_y_offset, width, border_height)
        pygame.draw.rect(self.surface, dark_green, self.up_side)

        self.right_side = pygame.Rect(width - border_width, board_y_offset + border_height, border_width,
                                      height - board_y_offset - 2 * border_height)
        pygame.draw.rect(self.surface, dark_green, self.right_side)

        self.down_side = pygame.Rect(0, height - border_height, width, border_height)
        pygame.draw.rect(self.surface, dark_green, self.down_side)
        pygame.display.flip()

    # Choosing the background image
    def render_background(self):

        self.surface.blit(bg, (0, board_y_offset))

        # im = Image.open("background.jpg")  # type:
        # M = im.size[0] // 2
        # N = im.size[1] // 2
        # tile = pygame.image.load(im.crop((0,0,32,32)))

        # self.surface.blit(tile, (200,200))
        # tiles = [im[x:x + M, y:y + N] for x in range(0, im.size[0], M) for y in range(0, im.size[1], N)]

    # Choosing the background image when is game over
    def render_gameover_background(self):
        bg = pygame.image.load("gameover.jpg")
        self.surface.blit(bg, (-1320, -620))

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
        # frameRate = self.speed
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
                        self.rottenapple.draw()
                        self.block.draw()
                        self.speedPotion.draw()
                        self.poison.draw()
                        self.reversepotion.draw()
                        pygame.display.flip()

                    # We make the different moves based on the key pressed if pause is True
                    if not pause:
                        if ((not self.snake.reversed_movement) and event.key == K_LEFT) or (
                                self.snake.reversed_movement and event.key == K_RIGHT):
                            if not (self.snake.x[1] < self.snake.x[0]):
                                self.snake.move_left()

                        elif ((not self.snake.reversed_movement) and event.key == K_RIGHT) or (
                                self.snake.reversed_movement and event.key == K_LEFT):
                            if not (self.snake.x[1] > self.snake.x[0]):
                                self.snake.move_right()

                        elif ((not self.snake.reversed_movement) and event.key == K_UP) or (
                                self.snake.reversed_movement and event.key == K_DOWN):
                            if not (self.snake.y[1] < self.snake.y[0]):
                                self.snake.move_up()

                        elif ((not self.snake.reversed_movement) and event.key == K_DOWN) or (
                                self.snake.reversed_movement and event.key == K_UP):
                            if not (self.snake.y[1] > self.snake.y[0]):
                                self.snake.move_down()

                # Making the game QUIT if the cross is pressed
                elif event.type == pygame.QUIT:

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
                print(grid)
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
