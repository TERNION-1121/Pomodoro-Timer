import pygame
from pathlib import Path

def fade(surface, screen, coord, r = 50):
        for alpha in range(r):
            surface.set_alpha(alpha)
            screen.blit(surface, coord)
            pygame.display.flip()
            pygame.time.delay(30)

def timer(screen):
    timerFont = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 80)
    time = timerFont.render("30:00", False, BLACK)
    screen.blit(time, ((width // 3), (height // 3) - 10))

# basic initilizations/setup
pygame.init()
pygame.font.init()
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
hasbegun = False
ticking = False
# background and colors
BG = (223, 235, 247) 
BLACK = (0, 0, 0)
GREY = (200, 210, 224)
DARK_GREY = (110, 112, 120)
WHITE = (228, 232, 247)
screen.fill(BG)
pygame.display.flip()

# font setup
header_font = pygame.font.Font('fonts\LexendGiga-Regular.ttf', 40)
button_font = pygame.font.Font('fonts\LexendGiga-Thin.ttf')
headerBG = pygame.Surface((450, 50))
buttonBG = pygame.Surface((70, 20))
headerBG.fill(BG)
buttonBG.fill(BG)

mainFont = header_font.render("Pomodoro Timer", False, BLACK)
readyFont = button_font.render("Ready?", False, BLACK)
beginFont = button_font.render("Begin!", False, BLACK)

fade(mainFont, screen, (192, 127))
pygame.draw.rect(screen, GREY, ((width // 2) - 10, 198, 70, 20))
fade(readyFont, screen, (width // 2, 200))
pygame.display.flip()

# event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse = pygame.mouse.get_pos()
        if not hasbegun and not ticking:
            if (width // 2) - 10 <= mouse[0] <= (width // 2) + 70 and 198 <= mouse[1] <= 218:
                pygame.draw.rect(screen, DARK_GREY, ((width // 2) - 10, 198, 70, 20))
                readyFont = button_font.render("Ready?", False, WHITE)
                screen.blit(readyFont, (width // 2, 200))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, GREY, ((width // 2) - 10, 198, 70, 20))
                    screen.blit(beginFont, (width // 2, 200))
                    pygame.display.flip()
                    for alpha in range(0, 256, 3):
                        headerBG.set_alpha(alpha)
                        buttonBG.set_alpha(alpha)
                        screen.blit(headerBG, (192, 127))
                        screen.blit(buttonBG, ((width // 2) - 10, 198))
                        pygame.display.flip()
                        pygame.time.delay(30)
                    hasbegun = True
                    ticking = True
            else:
                pygame.draw.rect(screen, GREY, ((width // 2) - 10, 198, 70, 20))
                readyFont = button_font.render("Ready?", False, BLACK)
                screen.blit(readyFont, (width // 2, 200))
            pygame.display.flip()

    if hasbegun:
        pomodoroText = header_font.render("Pomodoro", False, GREY)
        screen.blit(pomodoroText, (width // 3, (height // 3) + 20))
        pygame.display.flip()
        timer(screen)
                
pygame.quit()