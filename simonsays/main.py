import random
import pygame
import time

from pygame import font

from button import Button

# Initializes the pygame
pygame.init()

clock = pygame.time.Clock()
# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 227, 0)
RED_ON = (255, 0, 0)
RED_OFF = (227, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 227)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound("bell1.mp3")  # bell1
RED_SOUND = pygame.mixer.Sound("bell2.mp3")  # bell2
BLUE_SOUND = pygame.mixer.Sound("bell3.mp3")  # bell3
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3")  # bell4

green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 40)
red = Button(RED_ON, RED_OFF, RED_SOUND, 260, 40)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 290)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 290)

# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""
score = 0
prev_score_text = None
font = pygame.font.Font(None, 36)


def draw_board():
    global score

    # Remove old score text
    SCREEN.fill((0, 0, 0))
    # Render and display new score text
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))

    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)


'''
Chooses a random color and appends to cpu_sequence.
Illuminates randomly chosen color.
'''


def cpu_turn():
    print("\n\nCREATING NEW SEQUENCE")
    choice = random.choice(colors)  # pick random color
    cpu_sequence.append(choice)  # update cpu sequence
    if choice == "green":
        green.update(SCREEN)
    elif choice == "red":
        red.update(SCREEN)
    elif choice == "blue":
        blue.update(SCREEN)
    elif choice == "yellow":
        yellow.update(SCREEN)


'''
Plays pattern sequence that is being tracked by cpu_sequence
'''


def repeat_cpu_sequence():
    if len(cpu_sequence) != 0:
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)


'''
After cpu sequence is repeated the player must attempt to copy the same
pattern sequence.
The player is given 3 seconds to select a color and checks if the selected
color matches the cpu pattern sequence.
If player is unable to select a color within 3 seconds then the game is
over and the pygame window closes.
'''


def player_turn():
    turn_time = time.time()
    players_sequence = []
    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # button click occured
                # Grab the current position of mouse here
                pos = pygame.mouse.get_pos()
                if green.selected(pos):  # green button was selected
                    green.update(SCREEN)  # illuminate button
                    players_sequence.append("green")  # add to player sequence
                    check_sequence(players_sequence)  # check if playerchoice was correct
                    turn_time = time.time()  # reset timer
                elif red.selected(pos):
                    red.update(SCREEN)
                    players_sequence.append("red")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                elif blue.selected(pos):
                    blue.update(SCREEN)
                    players_sequence.append("blue")
                    check_sequence(players_sequence)
                    turn_time = time.time()

                elif yellow.selected(pos):
                    yellow.update(SCREEN)
                    players_sequence.append("yellow")
                    check_sequence(players_sequence)
                    turn_time = time.time()

        # If player does not select a button within 3 seconds then the gamecloses
    if not time.time() <= turn_time + 3:
        print("timer ran out...")
        game_over()


def check_sequence(players_sequence):
    global score
    print("checking sequence...")
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        print("INCORRECT")
        game_over()
    else:
        print("CORRECT")
        if len(players_sequence) == len(cpu_sequence):
            score += 1
            print("Players score: ", score)


'''
Quits game and closes pygame window
'''


def game_over():
    print("GAME OVER")
    pygame.quit()
    quit()


'''
Displays the remaining time as text on the window
'''

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    draw_board()  # Draw the buttons onto the pygame screen
    repeat_cpu_sequence()  # Repeat the CPU sequence if it's not empty
    cpu_turn()  # CPU randomly chooses a new color
    player_turn()  # Player tries to recreate CPU sequence
    pygame.time.wait(1000)  # Wait one second before repeating the CPU sequence
    clock.tick(60)

pygame.quit()
