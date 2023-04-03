import pygame

def fade(**surfacencoords: tuple):
    for alpha in range(0, 256, 3):
        for key in surfacencoords:
            surface, coordinates = surfacencoords[key]
            surface.set_alpha(alpha)
            screen.blit(surface, coordinates)
            pygame.time.delay(30)
        pygame.display.flip()

def timer(time: list):
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

def displayButton(rectColor: tuple, rectCoords: tuple, fontType: pygame.font.Font, fontText: str, fontColor: tuple, fontCoords: tuple, fadeFont = False):
    pygame.draw.rect(screen, rectColor, rectCoords)
    font = fontType.render(fontText, False, fontColor)
    if fadeFont:
        fade(s1c1 = (font, fontCoords))
    else:
        screen.blit(font, fontCoords)
    pygame.display.flip()

# basic initilizations/setup
pygame.init()
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# loop variables
running     =   True
startScreenFade     =   False
breakScreenFade  = False
endScreenFade = False
status      =   "end"

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
subheader_font_medium = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 55)
subheader_font_small = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 40)
subheader_font_large = pygame.font.Font('fonts\LexendGiga-ExtraLight.ttf', 80)
button_font = pygame.font.Font('fonts\LexendGiga-Thin.ttf')


# event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse = pygame.mouse.get_pos()

        match status:

            case "begin":
                if not startScreenFade:
                    mainFont = header_font.render("Pomodoro Timer", False, BLACK)
                    fade(s1c1 = (mainFont, (178, 128)))
                    displayButton(GREY, ((width // 2) - 30, 200, 70, 20), button_font, "Ready?", BLACK, (width // 2 - 20, 202), True)
                    startScreenFade = True

                elif (width // 2) - 10 <= mouse[0] <= (width // 2) + 70 and 198 <= mouse[1] <= 218:
                    displayButton(DARK_GREY, ((width // 2) - 30, 200, 70, 20), button_font, "Ready?", WHITE, (width // 2 - 20, 202))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        headerBG = pygame.Surface((450, 50))
                        buttonBG = pygame.Surface((70, 20))
                        headerBG.fill(BG)
                        buttonBG.fill(BG)
                        displayButton(GREY, (width // 2 - 30, 200, 70, 20), button_font, "Begin!", BLACK, (width // 2 - 20, 202))
                        fade(s1c1 = (headerBG, (178, 128)), s2c2 = (buttonBG, (width // 2 - 30, 200)))
                        status = "ticking"
                else:
                    displayButton(GREY, (width // 2 - 30, 200, 70, 20), button_font, "Ready?", BLACK, (width // 2 - 20, 202))

            case "ticking":
                timer([0, 1])
                finishedText = subheader_font_medium.render("Session Completed!", False, BLACK)
                fade(s1c1 = (finishedText,  (width - 725, height - 300)))
                status = "break"
            
            case "break":
                if not breakScreenFade:
                    displayButton(GREY, (318, 218, 150, 20), button_font, "Begin Break?", BLACK, (345, 220), True)
                    breakScreenFade = True
                elif 318 <= mouse[0] <= 468 and 218 <= mouse[1] <= 238:
                    displayButton(DARK_GREY, (318, 218, 150, 20), button_font, "Begin Break?", WHITE, (345, 220))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttonBG = pygame.Surface((150, 20))
                        headerBG = pygame.Surface((750, 60))
                        buttonBG.fill(BG)
                        headerBG.fill(BG)
                        displayButton(GREY, (318, 218, 150, 20), button_font, "Begin the chill!", BLACK, (335, 220))
                        fade(s1c1 = (buttonBG, (318, 218)), s2c2 = (headerBG, (30, 145)))
                        screen.fill(BG)
                        timer([0, 0])
                        status = "end"
                else:
                    displayButton(GREY, (318, 218, 150, 20), button_font, "Begin Break?", BLACK, (345, 220))
                
            case "end":
                endFont1 = subheader_font_small.render("Pomodoro Session", False, BLACK)
                endFont2 = subheader_font_large.render("Complete!", False, BLACK)
                if not endScreenFade:
                    fade(sc1 = (endFont1, (160, 100)), sc2 = (endFont2, (140, 130)))
                    displayButton(GREY, (200, 245, 130, 20), button_font, "Home Screen?", BLACK, (210, 247), True)
                    displayButton(GREY, (500, 245, 70, 20), button_font, "Quit?", BLACK, (514, 247), True)
                    endScreenFade = True
                elif 200 <= mouse[0] <= 330 and 245 <= mouse[1] <= 265:
                    displayButton(DARK_GREY, (200, 245, 130, 20), button_font, "Home Screen?", WHITE, (210, 247))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        startScreenFade = False
                        breakScreenFade = False
                        endScreenFade = False
                        status = "begin"
                        screen.fill(BG)
                elif 500 <= mouse[0] <= 570 and 245 <= mouse[1] <= 265:
                    displayButton(DARK_GREY, (500, 245, 70, 20), button_font, "Quit?", WHITE, (514, 247))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                else:
                    displayButton(GREY, (200, 245, 130, 20), button_font, "Home Screen?", BLACK, (210, 247))
                    displayButton(GREY, (500, 245, 70, 20), button_font, "Quit?", BLACK, (514, 247))
                
                    
pygame.quit()