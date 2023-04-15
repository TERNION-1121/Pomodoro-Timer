import pygame
import random
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
working_dir = os.getcwd().replace(r"\dist", "").replace(r"\pycache", "") + "\\"
music_dir = working_dir + r'\assets\songs'
icon = pygame.image.load(working_dir + r"assets\icons\pomodoro_timer.ico")
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
pygame.display.set_icon(icon)
pygame.display.set_caption("Pomodoro Timer")

# loop variables
running             = True
startScreenFaded    = False
breakScreenFaded    = False
bigBreakScreenFaded = False
endScreenFaded      = False
firstTick           = True
paused              = False
status              = "begin"

mainTimer  = [25, 0]
breakTimer = [5, 0]
bigBreakTimer = [20, 0]
totalSessionPeriod = 0
timeWidth = width // 3 - 30
timeHeight = height // 3 - 30

# background and colors
BG_LIGHT            = (223, 235, 247) 
BG_DARK             = (47, 49, 54)
TEXT_LIGHT          = (0, 0, 0)
TEXT_DARK           = (228, 232, 247)
BUTTON_LIGHT        = (200, 210, 224)
BUTTON_TEXT_LIGHT   = (0, 0, 0)
BUTTON_TEXT_DARK    = (255, 255, 255)
BUTTON_FOCUS_LIGHT  = (110, 112, 120)
BUTTON_FOCUS_DARK   = (235, 237, 243)
WHITE               = (228, 232, 247)

BG          = (BG_LIGHT, BG_DARK)
TEXT        = (TEXT_LIGHT, TEXT_DARK)
BUTTON      = (BUTTON_LIGHT, BG_DARK)
BUTTON_FOCUS= (BUTTON_FOCUS_LIGHT, BUTTON_FOCUS_DARK)
BUTTON_TEXT = (BUTTON_TEXT_LIGHT, BUTTON_TEXT_DARK)
colorIndex  = 0
screen.fill(BG[colorIndex])

# font setup
header_font             = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Regular.ttf', 40)
subheader_font_large    = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 80)
subheader_font_medium   = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 55)
subheader_font_small    = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 40)
basic_font              = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 27)
bold_font               = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Thin.ttf', 130)
button_font             = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Thin.ttf')
timer_font              = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 100)
note_font               = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 10)

# sound setup
birds_chirps = pygame.mixer.Sound(working_dir + r"assets\sound_effects\birds_chirp.mp3")
owl_hooting = pygame.mixer.Sound(working_dir + r"assets\sound_effects\owl_hooting.mp3")
button_select = pygame.mixer.Sound(working_dir + r"assets\sound_effects\button_select.mp3")
music_queue = (music_dir + r"\chill-lofi-song.mp3", music_dir + r"\embrace.mp3", music_dir + r"\empty-mind.mp3", music_dir + r"\let-it-go.mp3",
                music_dir + r"\lofi-chill.mp3", music_dir + r"\lofi-study.mp3", music_dir + r"\rain-and-nostalgia.mp3", music_dir + r"\spirit-blossom.mp3",
                music_dir + r"\the-weekend.mp3", music_dir + r"\watr-fluid.mp3", music_dir + r"\storm-clouds.mp3", music_dir + r'\Calm-and-Peaceful.mp3',
                music_dir + r"\serendipity.mp3", music_dir + r"\lost-in-thought", music_dir + r'\dreaming.mp3', music_dir + r'\lurk-late.mp3')