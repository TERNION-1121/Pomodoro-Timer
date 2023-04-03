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
running = True
status = "begin"
started = False
breakStarted = False
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


# event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse = pygame.mouse.get_pos()

        match status:

            case "begin":
                if not started:
                    mainFont = header_font.render("Pomodoro Timer", False, BLACK)
                    fade(s1c1 = (mainFont, (178, 128)))
                    displayButton(GREY, ((width // 2) - 30, 200, 70, 20), button_font, "Ready?", BLACK, (width // 2 - 20, 202), True)
                    started = True

                elif (width // 2) - 10 <= mouse[0] <= (width // 2) + 70 and 198 <= mouse[1] <= 218:
                    displayButton(DARK_GREY, ((width // 2) - 30, 200, 70, 20), button_font, "Ready?", WHITE, (width // 2 - 20, 202))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        headerBG = pygame.Surface((450, 50))
                        buttonBG = pygame.Surface((70, 20))
                        displayButton(GREY, (width // 2 - 30, 200, 70, 20), button_font, "Begin!", BLACK, (width // 2 - 20, 202))
                        fade(s1c1 = (headerBG, (178, 128)), s2c2 = (buttonBG, (width // 2 - 30, 200)))
                        status = "ticking"
                else:
                    displayButton(GREY, (width // 2 - 30, 200, 70, 20), button_font, "Ready?", BLACK, (width // 2 - 20, 202))

            case "ticking":
                timer([0, 1])
                finishedText = subheader_font.render("Session Completed!", False, BLACK)
                fade(s1c1 = (finishedText,  (width - 725, height - 300)))
                status = "break"
            
            case "break":
                if not breakStarted:
                    displayButton(GREY, (318, 218, 150, 20), button_font, "Begin Break?", BLACK, (345, 220), True)
                    breakStarted = True
                elif (width // 2) - 50 <= mouse[0] <= (width // 2) + 50 and 218 <= mouse[1] <= 238:
                    displayButton(DARK_GREY, (318, 218, 150, 20), button_font, "Begin Break?", WHITE, (345, 220))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttonBG = pygame.Surface((150, 20))
                        buttonBG.fill(BG)
                        displayButton(GREY, (318, 218, 150, 20), button_font, "Begin the chill!", BLACK, (335, 220))
                        fade(s1c1 = (buttonBG, (318, 218)))
                        screen.fill(BG)
                        timer([0, 0])
                        status = "begin"
                        started = False
                        breakStarted = False
                else:
                    displayButton(GREY, (318, 218, 150, 20), button_font, "Begin Break?", BLACK, (345, 220))
                
pygame.quit()