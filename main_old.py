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
counter = 0
counting = False
##################################################################################################################################################################################################

# General setup
pygame.init()
clock = pygame.time.Clock()

# Creating a class for the snake
class Snake():
    # laoding the block on the screen and giving length as an atribute
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("snake.png")
        self.direction = 'down'

        # Starting length for the snake
        self.length = length

        # Positions of the snake blocks, we multiply it by the length so it create a list for all the snake blocks positions we want
        self.x = [72] * length
        self.y = [316] * length

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
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update the position of the first block based on the direction
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    # Creating different blocks of the snake at the beginning of the game
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

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

        # We have to pop the last block of the snake so we put -1
        self.x.pop(-1)
        self.y.pop(-1)

    # Creating a function to count the number of apples eaten by the snake
    def counting(self):
        self.counter += 1
        if game.high_score < self.counter:
            game.high_score += 1

# Creating a class for the object apple
class Apple():
    # Setting the screen for apple and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png")
        self.x = 104
        self.y = 348
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

# Creating a class for the object rottenapple
class RottenApple:
    # Setting the screen for rottenapple and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("rotten_apple.png")
        self.x = 136
        self.y = 380
        self.set_poison_x =  [136]
        self.set_poison_y = [380]

    # drawing the poison object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Creating a function to move the poison randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28

# Creating a class for the object block
class Block():
    # Setting the screen for apple and creating its positions
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.image = pygame.image.load("block.png")
        self.x = 168
        self.y = 412
        self.set_block_x =  [168]
        self.set_block_y = [412]

    # Creating a function to draw the apple object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Creating new Blocks
    #def new_blocks(self):
        #self.new_x = random.randint(1, 35) * SIZE + 8
        #self.new_y = random.randint(4, 27) * SIZE + 28
        #self.parent_screen.blit(self.image, (self.new_x, self.new_y))
        #pygame.display.flip()

# Creating a class for the potion object
class Potion:
    # Setting the screen for potion and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("potion.png")
        self.x = 200
        self.y = 444

    # Creating a function to draw the poitoin object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Creating a function to move the potion randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28

    # Creating a function to move the potion outside the screen
    def move_outside(self):
        self.x = 3000
        self.y = 3000

# Creating a class for the object Poision
class Poison:
    # Setting the screen for poison and creating its positions
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("poison.png")
        self.x = 232
        self.y = 476
        self.set_poison_x =  [136]
        self.set_poison_y = [380]

    # drawing the poison object
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Creating a function to move the poison randomly whenever it gets eaten by the snake
    def move(self):
        self.x = random.randint(1, 35) * SIZE + 8
        self.y = random.randint(4, 27) * SIZE + 28

    # Creating a function to move the potion outside the screen
    def move_outside(self):
        self.x = 3200
        self.y = 3200

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
        self.speed = 0.1 

        # Setting up the main window
        self.surface  = pygame.display.set_mode((1200, 960))
        
        # Setting the background music and the sounds
        pygame.mixer.init()
        # self.play_background_music()

        # Creating a class snake and drawing it
        self.snake = Snake(self.surface, 1)
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
        self.potion = Potion(self.surface)
        self.potion.draw()

         # Creating a class poison and drawing it
        self.poison = Poison(self.surface)
        self.poison.draw()

    # Creating a function to play the background music
    def play_background_music(self):
        pygame.mixer.music.load('MP3.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0)

    # Creating a function to play the different sound effects 
    def play_sound(self, sound_name):
        if sound_name == "game over":
            sound = pygame.mixer.Sound("game over.mp3")
            sound.play()
        elif sound_name == 'eating':
            sound = pygame.mixer.Sound("eating.mp3")
            sound.play()
        elif sound_name == "woosh":
            sound = pygame.mixer.Sound("woosh.mp3")
            sound.play()
        elif sound_name == "slow":
            sound = pygame.mixer.Sound("slow.mp3")
            sound.play()
        elif sound_name == "vomit":
            sound = pygame.mixer.Sound("vomit.mp3")
            sound.play()

    # We must create boundaries for the snake to stay in the green zone
    def boundaries(self, x1, y1):
        if (x1 < 40) or (x1 > 1159) or (y1 < 155) or (y1 > 923):
            return True
        return False

    # Creating the reset function when the player presses the enter button   
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.rottenapple = RottenApple(self.surface)
        self.block = Block(self.surface, 1)
        self.potion = Potion(self.surface)
        self.poison = Poison(self.surface)


    # Creating a function when there is a collision happening between the snake and other objects
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
        
    def play(self):

        # Creating the background, visuals, and the objects on the screen
        self.render_background()
        self.game_visuals()
        self.snake.walk()
        self.apple.draw()
        self.rottenapple.draw()
        self.block.draw()
        self.potion.draw()
        self.poison.draw()
        pygame.display.flip()

        # ALL THE CONDITIONS FOR THE DIFFERENT COLLISIONS:

        # Snake eating the poison when has a length of 1, avoiding score of -1 at the beggining
        if self.snake.length == 1:
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.rottenapple.x, self.rottenapple.y):
                self.play_sound('game over')
                raise "Collision Occurred"

        # Snake hitting the boundaries of the game(4 different sides)
        if self.boundaries(self.snake.x[0], self.snake.y[0]) == True:
            
            self.play_sound('game over')
            raise "Collision Occurred"

        # snake hitting the apple(eating it)
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eating")
            self.snake.increase_length()
            self.snake.counting()
            self.apple.move()
            self.load_game_info_screen()
            
        # snake eating rottenapple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.rottenapple.x, self.rottenapple.y):
            self.play_sound("vomit")
            self.rottenapple.move()
            self.snake.decrease_length()

        # snake eating potion
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.potion.x, self.potion.y):
            self.play_sound("woosh")

            # Making the snake faster 
            self.speed -= 0.09

            if self.speed < 0.02:
                self.potion.move_outside()
            else:
                self.potion.move()

            # Moving the poison object to the screen
            if self.poison.x > 2000:
                self.poison.move()

          # snake eating poison
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.poison.x, self.poison.y):
            self.play_sound("slow")

            # Making the snake slower 
            self.speed += 0.09

            if self.speed == 0.19:
                self.poison.move_outside()
            else:
                self.poison.move()
            
            # Moving the potion object to the screen
            if self.potion.x > 2000:
                self.potion.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('game over')
                raise "Collision Occurred"

        # snake hitting the block(eating it)
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.block.x, self.block.y):
            self.play_sound('game over')
            raise "Collision Occurred"

    # for displaying the score of the player
    def display_score(self):
        font = pygame.font.SysFont('arial',70)

        # We use the counter to display the score of the player
        score = font.render(f"Score: {self.snake.counter}",True,(0,0,0))
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

    # for displaying the number of blocks on the screen
    def display_number_blocks(self):
        font = pygame.font.SysFont('arial',70)

        # We use the second counter to display the score of the player
        score = font.render(f"Blocks: 1",True,(0,0,0))
        self.surface.blit(score,(370,10))

        pygame.display.flip()

    # VISUALS

    # making the highest score
    def display_hihgest_score(self):
        font = pygame.font.SysFont('arial',70)

        # We use the counter to display the score of the player
        score = font.render(f"Highest Score: {self.high_score}",True,(0,0,0))
        self.surface.blit(score,(750,10))

        pygame.display.flip()

    # making visuals of the game infor screen 
    def load_game_info_screen(self):
        
        self.info_screen = pygame.Rect( 0, 0, 1200, 120)
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
        bg = pygame.image.load("background.jpg")
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
        game.load_game_info_screen()
        while running:

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


                    # We make the different moves based on the key pressed if pause is True
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                # Making the game QUIT if the cross is pressed
                elif event.type  == pygame.QUIT:

                    # updating highest score
                    self.saving_high_score()
                    
                    running = False
            
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                        
            # Updaiting the wondow
            clock.tick(60)
            time.sleep(self.speed)

if __name__ == '__main__':
    game = Game()
    game.run()

# Tomorrow: Fix the positioning of the blocks so that they don't end up on each other, for the apple and other objects
