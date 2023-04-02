import pygame
from pathlib import Path

def fade(surface, coord, r = 50):
        for alpha in range(r):
            surface.set_alpha(alpha)
            screen.blit(surface, coord)
            pygame.display.flip()
            pygame.time.delay(30)

def timer(time):
    timerFont = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 100)
    for minute in range(time[0], -1, -1):
        for seconds in range(time[1], -1, -1):
            print(f"{minute:02d}:{seconds:02d}")
            timeText = timerFont.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
            screen.blit(timeText, ((width // 3) - 30, (height // 3) - 30))
            pygame.display.flip()
            pygame.time.delay(900)
            timeText = timerFont.render(f"{minute:02d}:{seconds:02d}", False, BG)
            screen.blit(timeText, ((width // 3) - 30, (height // 3) - 30))
            pygame.display.flip()
        if time[1] == 0:
            time[1] = 59

def displayButton(rectColor, rectCoords, fontType, fontText, fontColor, fontCoords, fadeFont = False):
    pygame.draw.rect(screen, rectColor, rectCoords)
    font = fontType.render(fontText, False, fontColor)
    if fadeFont:
        fade(font, (width // 2, 200))
    else:
        screen.blit(font, fontCoords)
    pygame.display.flip()

# basic initilizations/setup
pygame.init()
pygame.font.init()
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
end = False
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
subheader_font = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 55)
button_font = pygame.font.Font('fonts\LexendGiga-Thin.ttf')
headerBG = pygame.Surface((450, 50))
buttonBG = pygame.Surface((70, 20))
headerBG.fill(BG)
buttonBG.fill(BG)

mainFont = header_font.render("Pomodoro Timer", False, BLACK)
readyFont = button_font.render("Ready?", False, BLACK)
beginFont = button_font.render("Begin!", False, BLACK)

fade(mainFont, (192, 127))
displayButton(GREY, ((width // 2) - 10, 198, 70, 20), button_font, "Ready?", BLACK, (width // 2, 200), True)

# event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse = pygame.mouse.get_pos()
        if (width // 2) - 10 <= mouse[0] <= (width // 2) + 70 and 198 <= mouse[1] <= 218:
            displayButton(DARK_GREY, ((width // 2) - 10, 198, 70, 20), button_font, "Ready?", WHITE, (width // 2, 200))
            if event.type == pygame.MOUSEBUTTONDOWN:
                displayButton(GREY, ((width // 2) - 10, 198, 70, 20), button_font, "Begin!", BLACK, (width // 2, 200))
                for alpha in range(0, 256, 3):
                        headerBG.set_alpha(alpha)
                        buttonBG.set_alpha(alpha)
                        screen.blit(headerBG, (192, 127))
                        screen.blit(buttonBG, ((width // 2) - 10, 198))
                        pygame.display.flip()
                        pygame.time.delay(30)
                timer([0, 3])
                finishedText = subheader_font.render("Session Completed!", False, BLACK)
                fade(finishedText,  ((width - 725), (height - 300)))
                while True:
                    print(mouse)
                    if (width // 2) - 10 <= mouse[0] <= (width // 2) + 100 and 218 <= mouse[1] <= 238:
                        displayButton(DARK_GREY, ((width // 2) - 10, 218, 110, 20), button_font, "Begin Break?", WHITE, (width // 2, 220))
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            screen.fill(BG)
                            timer([0, 2])
                            break
                    else:
                        displayButton(GREY, ((width // 2) - 10, 218, 110, 20), button_font, "Begin Break?", BLACK, (width // 2, 220))                      
        else:
            displayButton(GREY, ((width // 2) - 10, 198, 70, 20), button_font, "Ready?", BLACK, (width // 2, 200))
                
                
pygame.quit()