import pygame
import time
import os

def fade(*surfacencoords: tuple):
    for alpha in range(0, 257, 6):
        for snc in surfacencoords:
            surface, coordinates = snc
            surface.set_alpha(alpha)
            screen.blit(surface, coordinates)
            pygame.time.delay(30)
        pygame.display.flip()

def displayButton(**buttons: tuple):
    buttonsToFade = []
    for button in buttons:
        rectData, fontData = buttons[button]
        rectColor, rectCoords = rectData
        pygame.draw.rect(screen, rectColor, rectCoords)
        font = fontData[0].render(fontData[1], False, fontData[2])
        if fontData[4]:
            buttonsToFade.append((font, fontData[3]))
        else:
            screen.blit(font, fontData[3])
    pygame.display.flip()
    fade(*buttonsToFade)

pygame.init()

# basic initilizations/setup
working_dir = os.getcwd().replace(r"\dist", "") + "\\"
icon = pygame.image.load(working_dir + r"assets\icons\pomodoro_timer.ico")
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(icon)
pygame.display.set_caption("Pomodoro Timer")

# loop variables
running             = True
startScreenFaded    = False
breakScreenFaded    = False
endScreenFaded      = False
firstTick           = True
status              = "begin"

mainTimer = [30, 0]
breakTimer = [5, 0]
timeWidth = width // 3 - 30
timeHeight = height // 3 - 30

# background and colors
BG          = (223, 235, 247) 
BLACK       = (0, 0, 0)
GREY        = (200, 210, 224)
DARK_GREY   = (110, 112, 120)
WHITE       = (228, 232, 247)
screen.fill(BG)

# font setup
header_font             = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Regular.ttf', 40)
subheader_font_medium   = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 55)
subheader_font_small    = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 40)
subheader_font_large    = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 80)
button_font             = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Thin.ttf')
timer_font              = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 100)

# sound setup
button_select = pygame.mixer.Sound(working_dir + r"assets\sound_effects\button_select.mp3")