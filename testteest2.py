###################################################################################Imports & Constants#############################################################################################
import pygame
import sys
from pygame.locals import *
import main
from pygame import mixer

##################################################################################################################################################################################################
game_2 = main.Game()

play_sound = True

# initializing the pygame
pygame.init()

# Setting the clicking sound effect
click = pygame.mixer.Sound("click.mp3")

# Setting up the main window
screen_width = 970
screen_height = 1022
screen = pygame.display.set_mode((screen_width, screen_height))

# Creating the caption of the game
pygame.display.set_caption('Snake Game')

# Creating a function to play the background music
def play_background_music():
    pygame.mixer.music.load('intro.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0)

# Creating a class for the bottons in the main menu
class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attribute 
        self.pressed = False
        self.elevaton = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # Creating the top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#354B5E'
        
        # Creating the color of the rectangle
        self.top_color = '#ddd1b2'

        # text 
        font_1 = pygame.font.SysFont('comicsans',50)
        self.text_surf = font_1.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    # Drawing the rectangles 
    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 25)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 25)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def checkForInput(self, position):
        if position[0] in range(self.top_rect.left, self.top_rect.right) and position[1] in range(self.top_rect.top, self.top_rect.bottom):
            return True
        return False

    # Checking if the button is clicked
    def check_click(self):
        # action = False
        mouse_pos = pygame.mouse.get_pos()
        if not self.top_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.pressed = True
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#cab784'
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                # action = True
                self.dynamic_elevation = 0
                self.pressed = True
                print('click1')
                return True
            if not pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = self.elevaton
                if self.pressed == True:
                    print('click2')
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevaton
            self.top_color = '#ddd1b2'
        #return action

# General setup
clock = pygame.time.Clock()

# Creating a unique color for the Rectangels
creamy = (198, 189, 171)

# Game Rectangles
up_side = pygame.Rect( 0, 0, 970, 62)
left_side = pygame.Rect( 0, 62, 201, 600)
right_side = pygame.Rect(799 , 62, 201, 600)
down_side = pygame.Rect( 0, 661, 1000, 360)

# Game_mode Rectangles
creative_game = pygame.Rect( 0, 0, 970, 62)
survival_game = pygame.Rect( 0, 62, 201, 600)
opponent_game = pygame.Rect(799 , 62, 201, 600)

# Texts and fonts on the screen
font = pygame.font.SysFont('comicsans',80)
font_2 = pygame.font.SysFont('comicsans',60)
snake = font.render(f"SNAKE",True,(176, 132, 132))
game = font.render(f"GAME",True,(176, 132, 132))
volume = font_2.render(f"Volume",True,(0, 0, 0))
sound = font_2.render(f"Sound",True,(0, 0, 0))

# Creating different buttons
play_button = Button('Start Game', 290, 80, (340, 630), 6)
options_button = Button('Options', 230, 80, (640, 830), 6)
help_button = Button('Help', 200, 80, (130, 830), 6)
Game_mode_button = Button('Game Mode', 300, 80, (170, 730), 6)
Difficulty_button = Button('Difficulty', 300, 80, (490, 730), 6)
exit_button = Button('Exit Game', 250, 80, (360, 830), 6)
back_button  = Button('Back', 180, 80, (85, 850), 6)

# Initializing the background music
pygame.mixer.init()
play_background_music()

# Creating another class for the volume button on the option menu
class Button_2(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button_2, self).__init__()

        # Core attribute 
		self.image = img
		self.scale = scale
		self.image = pygame.transform.scale(self.image, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

    # Creating a function to update the image every time we click on it
	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

    # Creating a function to check if the button is clicked or not
	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action 

# loading different images 
music_on = pygame.image.load('volume.png')
music_off = pygame.image.load('mute.png')
sound_on = pygame.image.load('sound-on.png')
sound_off = pygame.image.load('sound-off.png')
right_can = pygame.image.load('right_can.png')
left_can = pygame.image.load('left_can.png')
right_cant = pygame.image.load('right_cant.png')
right_cant_img = pygame.transform.scale(right_cant, (70, 70))
left_cant = pygame.image.load('left_cant.png')
left_cant_img = pygame.transform.scale(left_cant, (70, 70))


# Creating a music button
music_btn = Button_2(music_on, (90, 90), 550, 250)

# Creating a sound button
sound_btn = Button_2(sound_on, (90, 90), 550, 380)

# Creating a right and a left button
right_button_can = Button_2(right_can, (70, 70), 545, 850)
left_button_can = Button_2(left_can, (70, 70), 435, 850)

# Creating a function for the border of the screen
def visuals():
    
    # loading the border image
    cobra = pygame.image.load("cobra.png")

    # Visuals and printing them
    screen.blit(cobra, (5,5))
    screen.blit(cobra, (5,68))
    screen.blit(cobra, (5,131))
    screen.blit(cobra, (5,194))
    screen.blit(cobra, (5,257))
    screen.blit(cobra, (5,320))
    screen.blit(cobra, (5,383))
    screen.blit(cobra, (5,446))
    screen.blit(cobra, (5,509))
    screen.blit(cobra, (5,572))
    screen.blit(cobra, (5,635))
    screen.blit(cobra, (5,698))
    screen.blit(cobra, (5,761))
    screen.blit(cobra, (5,824))
    screen.blit(cobra, (5,887))
    screen.blit(cobra, (5,949))
    screen.blit(cobra, (901,5))
    screen.blit(cobra, (901,68))
    screen.blit(cobra, (901,131))
    screen.blit(cobra, (901,194))
    screen.blit(cobra, (901,257))
    screen.blit(cobra, (901,320))
    screen.blit(cobra, (901,383))
    screen.blit(cobra, (901,446))
    screen.blit(cobra, (901,509))
    screen.blit(cobra, (901,572))
    screen.blit(cobra, (901,635))
    screen.blit(cobra, (901,698))
    screen.blit(cobra, (901,761))
    screen.blit(cobra, (901,824))
    screen.blit(cobra, (901,887))
    screen.blit(cobra, (69,949))
    screen.blit(cobra, (133,949))
    screen.blit(cobra, (197,949))
    screen.blit(cobra, (261,949))
    screen.blit(cobra, (325,949))
    screen.blit(cobra, (389,949))
    screen.blit(cobra, (453,949))
    screen.blit(cobra, (517,949))
    screen.blit(cobra, (581,949))
    screen.blit(cobra, (645,949))
    screen.blit(cobra, (709,949))
    screen.blit(cobra, (773,949))
    screen.blit(cobra, (837,949))
    screen.blit(cobra, (901,949))
    screen.blit(cobra, (69,5))
    screen.blit(cobra, (133,5))
    screen.blit(cobra, (197,5))
    screen.blit(cobra, (261,5))
    screen.blit(cobra, (325,5))
    screen.blit(cobra, (389,5))
    screen.blit(cobra, (453,5))
    screen.blit(cobra, (517,5))
    screen.blit(cobra, (581,5))
    screen.blit(cobra, (645,5))
    screen.blit(cobra, (709,5))
    screen.blit(cobra, (773,5))
    screen.blit(cobra, (837,5))

# Creating the information for the options menu
def load_info_images(): 
        
        # For the snake image
        snake_image = pygame.image.load("snake_big.png")
        screen.blit(snake_image, (130, 210))

        # For the apple image
        apple_image = pygame.image.load("apple_big.png")
        screen.blit(apple_image, (130, 310))

        # For the rottenapple image
        rotten_apple_image = pygame.image.load("rotten_apple_big.png")
        screen.blit(rotten_apple_image, (130, 410))

        # For the potion image
        speed_potion_image = pygame.image.load("potion_big.png")
        screen.blit(speed_potion_image, (130, 510))

        # For the poison image
        poison_image = pygame.image.load("poison_big.png")
        screen.blit(poison_image, (130, 610))
        
        # For the block image
        block_image = pygame.image.load("block_big.png")
        screen.blit(block_image, (130, 720))

# Creating the information for the options menu
def load_info_images_2():

    # For the reverse potion image
        image_1 = pygame.image.load("reversepotion_big.png")
        screen.blit(image_1, (120, 220))

    # For the slow death potion image
        image_2 = pygame.image.load("slow_death_big.png")
        screen.blit(image_2, (120, 355))

    # For the translucent potion image
        image_3 = pygame.image.load("translucent_potion_big.png")
        screen.blit(image_3, (120, 490))

# Printing the Volume image
def load_volume_image():
        image_1 = pygame.image.load("volume.png")
        screen.blit(image_1, (800, 100))

# Printing the mute image
def load_mute_image():
        image_1 = pygame.image.load("mute.png")
        screen.blit(image_1, (130, 210))

# Creating a function for when the option button is pressed
def options_menu():
    music_on_1 = True
    sound_on_1 = True

    global play_sound
    
    while True:

        screen = pygame.display.set_mode((970, 1022))

        # getting rid of the previous images in the main menu
        screen.fill(creamy)

        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(220,70))
        screen.blit(game,(530,70))
        screen.blit(volume,(260,245))
        screen.blit(sound,(260,375))

        # Drawing the 'back' button
        back_button.draw()
        
        # Drawing the music buttton
        if music_btn.draw(screen):
            if play_sound:
                pygame.mixer.Sound.play(click)
            music_on_1 = not music_on_1

            if music_on_1:
                music_btn.update_image(music_on)
                pygame.mixer.music.unpause()
            else:
                music_btn.update_image(music_off)
                pygame.mixer.music.pause()

        # Drawing the sound button
        if sound_btn.draw(screen):
            
            sound_on_1 = not sound_on_1

            if sound_on_1:
                pygame.mixer.Sound.play(click)
                sound_btn.update_image(sound_on)
                play_sound = True
            else:
                sound_btn.update_image(sound_off)
                play_sound = False

        pygame.display.update()
        
        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                main_menu()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)

# Creating a function for when the Game Mode button is pressed
def Game_mode_menu():

    global play_sound

    while True:

        screen = pygame.display.set_mode((970, 1022))

        # getting rid of the previous images in the main menu
        screen.fill(creamy)

        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(220,70))
        screen.blit(game,(530,70))

         # Visuals 
        pygame.draw.rect(screen, creamy, creative_game)
        pygame.draw.rect(screen, creamy, survival_game)
        pygame.draw.rect(screen, creamy, opponent_game)
        
        # Drawing the 'back' button
        back_button.draw()
        
        
        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                main_menu()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)

# Creating a function for when the difficulty button is pressed
def difficulty_menu():
    #sound_on = True

    # pygame.mixer.init()
    # play_background_music()

    while True:

        screen = pygame.display.set_mode((970, 1022))

        # getting rid of the previous images in the main menu
        screen.fill(creamy)

        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(150,70))
        screen.blit(game,(450,70))
 
        # Drawing the 'back' button
        back_button.draw()
        
        
        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                main_menu()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)

# Creating a function for when the help button is pressed
def help_menu():
    sound_on = True
    right_on = False

    # pygame.mixer.init()
    # play_background_music()

    while True:

        screen = pygame.display.set_mode((970, 1022))

        # getting rid of the previous images in the main menu
        screen.fill(creamy)

        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(220,70))
        screen.blit(game,(530,70))

        # Discription of the icons
        # Snake Discription
        font1 = pygame.font.SysFont('arial', 30)
        line1 = font1.render(f"This is you, the Snake icon! You will use your direction keys ", True, (0, 0, 0))
        line1_2 = font1.render(f"to move it around and have fun!! ", True, (0, 0, 0))
        screen.blit(line1, (215,205))
        screen.blit(line1_2, (215, 235))

        # Apple description
        line2 = font1.render(f"This is the apple icon! When you eat the apple, your length ", True, (0, 0, 0))
        line2_2 = font1.render(f"will increase by one, eat a lot of them!! ", True, (0, 0, 0))
        screen.blit(line2, (215,310))
        screen.blit(line2_2, (215, 340))

        # Rottenapple description
        line3 = font1.render(f"This is the rotten apple icon! When you eat the rotten apple ", True, (0, 0, 0))
        line3_2 = font1.render(f"your length will decrease by one, try not to eat them!! ", True, (0, 0, 0))
        screen.blit(line3, (215,410))
        screen.blit(line3_2, (215, 440))

        # Speed Potion descripti0n 
        line4 = font1.render(f"This is the speed potion icon! When you eat the potion, your", True, (0, 0, 0))
        line4_2 = font1.render(f"speed will become faster. Once you reach a score of 5, you", True, (0, 0, 0))
        line4_3 = font1.render(f"can use this potion!!", True, (0, 0, 0))
        screen.blit(line4, (215,500))
        screen.blit(line4_2, (215, 530))
        screen.blit(line4_3, (215, 560))

        # Poison descripti0n 
        line5 = font1.render(f"This is the poison icon! When you eat the poison, your speed ", True, (0, 0, 0))
        line5_2 = font1.render(f"will become slower. Once you reach a score of 5, you can use", True, (0, 0, 0))
        line5_3 = font1.render(f"this potion!", True, (0, 0, 0))
        screen.blit(line5, (215,610))
        screen.blit(line5_2, (215, 640))
        screen.blit(line5_3, (215, 670))

        # Block descripti0n 
        line6 = font1.render(f"This is the block icon! If you hit the block, the game will", True, (0, 0, 0))
        line6_2 = font1.render(f"be over immediately!! Its number will increase every time", True, (0, 0, 0))
        line6_3 = font1.render(f"you eat an apple!!", True, (0, 0, 0))
        screen.blit(line6, (215,720))
        screen.blit(line6_2, (215, 750))
        screen.blit(line6_3, (400, 780))
 
        # Drawing the 'back' button
        back_button.draw()

        # Drawing the right button
        if right_button_can.draw(screen):
            if play_sound:
                pygame.mixer.Sound.play(click)
            right_on = not right_on

            if right_on:
                help_menu_2()
            else:
                pass

        # Drawing the left button
        screen.blit(left_cant_img, (435, 850))
        
        load_info_images()

        pygame.display.update()
        
        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                main_menu()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)
        
# Creating a function for when the next page of the help menu is pressed:
def help_menu_2():
    sound_on = True
    left_can_on = True

    global play_sound
    
    while True:

        screen = pygame.display.set_mode((970, 1022))

        # getting rid of the previous images in the main menu
        screen.fill(creamy)

        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(220,70))
        screen.blit(game,(530,70))

        # Discription of the other icons
        # Reverse Potion discription
        font1 = pygame.font.SysFont('arial', 30)
        line1 = font1.render(f"This is the reverse potion! When you eat this potion, all your ", True, (0, 0, 0))
        line1_2 = font1.render(f"directions would get reversed for five seconds. You will see", True, (0, 0, 0))
        line1_3 = font1.render(f"this potion once your score gets above 10, BE CAREFUL!", True, (0, 0, 0))
        screen.blit(line1, (210,205))
        screen.blit(line1_2, (210, 235))
        screen.blit(line1_3, (210, 265))

        # Slow death potion description
        line2 = font1.render(f"This is the slow death potion! When you each this potion,", True, (0, 0, 0))
        line2_2 = font1.render(f"your length starts to decrease 1 block per second!! The only", True, (0, 0, 0))
        line2_3 = font1.render(f"way to stop this is by eating an apple. Don't worry, you will", True, (0, 0, 0))
        line2_4 = font1.render(f"not see it unless your score is above 20!!", True, (0, 0, 0))
        screen.blit(line2, (230,330))
        screen.blit(line2_2, (210, 360))
        screen.blit(line2_3, (210, 390))
        screen.blit(line2_4, (280, 420))

        # Translucent potion description
        line3 = font1.render(f"This is the translucent potion! When you eat this potion, you ", True, (0, 0, 0))
        line3_2 = font1.render(f"can go through any blocks for 5 seconds! Once you reach a", True, (0, 0, 0))
        line3_3 = font1.render(f"score of 15, you can see this potion and eat it!!", True, (0, 0, 0))
        screen.blit(line3, (210,485))
        screen.blit(line3_2, (210, 515))
        screen.blit(line3_3, (210, 545))

        # Drawing the right button
        screen.blit(right_cant_img, (545, 850))
                
        # Drawing the left button
        if left_button_can.draw(screen):
            if play_sound:
                pygame.mixer.Sound.play(click)
            left_can_on = not left_can_on

            if left_can_on:
                pass
            else:
                help_menu()

        # Loading the images of icons
        load_info_images_2()
        
        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                main_menu()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)

def main_menu():

    global play_sound
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    while True:

        # creating the background image
        menu_screen = pygame.image.load("menu.jpg")
        resized_menu = pygame.transform.scale(menu_screen, (600, 600))
        screen.blit(resized_menu, (200,62))

        # Visuals 
        pygame.draw.rect(screen, creamy, down_side)
        pygame.draw.rect(screen, creamy, left_side)
        pygame.draw.rect(screen, creamy, right_side)
        pygame.draw.rect(screen, creamy, up_side)
        
        # Printing the visuals 
        visuals()

        # Texts
        screen.blit(snake,(70,100))
        screen.blit(game,(630,100))

        # Drawing the buttons
        play_button.draw()
        options_button.draw()
        exit_button.draw()
        help_button.draw()
        Game_mode_button.draw()
        Difficulty_button.draw()

        #Handling input
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
               
                pygame.quit()
                sys.exit()
            if play_button.checkForInput(MENU_MOUSE_POS):
                if play_sound:
                    pygame.mixer.Sound.play(click)
                game_2.__init__()
                game_2.run()
                pygame.quit()
            elif Game_mode_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                Game_mode_menu()
            elif Difficulty_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                difficulty_menu()
            elif options_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                options_menu()
            elif help_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                help_menu()
            elif exit_button.check_click():
                if play_sound:
                    pygame.mixer.Sound.play(click)
                pygame.quit()
                sys.exit()

        # Updaiting the wondow
        pygame.display.flip()
        clock.tick(60)
main_menu()
