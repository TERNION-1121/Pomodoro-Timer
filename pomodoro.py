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

# basic initilizations/setup
pygame.init()
working_dir = os.getcwd().replace(r"\dist", "") + '\\'
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pomodoro Timer")
icon = pygame.image.load(working_dir + r"assets\Pomodoro_Timer_Icon.png")
pygame.display.set_icon(icon)

# loop variables
running          = True
startScreenFaded = False
breakScreenFaded = False
endScreenFaded   = False
firstTick = True
status           = "begin"
timer = [30, 0]
breakTimer = [5, 0]
timeWidth = width // 3 - 30
timeHeight = height // 3 - 30

# background and colors
BG      = (223, 235, 247) 
BLACK   = (0, 0, 0)
GREY    = (200, 210, 224)
DARK_GREY   = (110, 112, 120)
WHITE       = (228, 232, 247)
screen.fill(BG)

# font setup
header_font = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Regular.ttf', 40)
subheader_font_medium = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 55)
subheader_font_small = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 40)
subheader_font_large = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 80)
button_font = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-Thin.ttf')

timer_font = pygame.font.Font(working_dir + r'assets\fonts\LexendGiga-ExtraLight.ttf', 100)

# sound setup
button_select = pygame.mixer.Sound(working_dir + r"assets\sound_effects\button_select.mp3")

# event loop
while running:  
        iTime = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()
        match status:

            case "begin":
                rectCoordinates = (width // 2 - 30, 200, 70, 20)
                textCoordinates = (width // 2 - 20, 202)

                if not startScreenFaded:
                    mainFont = header_font.render("Pomodoro Timer", False, BLACK)
                    fade((mainFont, (178, 128)))
                    pygame.time.delay(1000)

                    displayButton(b = ((GREY, rectCoordinates), (button_font, "Ready?", BLACK, textCoordinates, True)))

                    startScreenFaded = True

                elif (width // 2) - 30 <= mouse[0] <= (width // 2) + 40 and 200 <= mouse[1] <= 220:
                    displayButton(b = ((DARK_GREY, rectCoordinates), (button_font, "Ready?", WHITE, textCoordinates, False)))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.Sound.play(button_select)

                        headerBG = pygame.Surface((450, 50))
                        buttonBG = pygame.Surface((70, 20))
                        headerBG.fill(BG)
                        buttonBG.fill(BG)

                        displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin!", BLACK, textCoordinates, False)))
                        fade((headerBG, (178, 128)), (buttonBG, (width // 2 - 30, 200)))

                        status = "ticking"
                else:
                    displayButton(b = ((GREY, (width // 2 - 30, 200, 70, 20)), (button_font, "Ready?", BLACK, (width // 2 - 20, 202), False)))

            case "ticking":
                dt = time.time() - iTime
                timer[1] = timer[1] - int(dt) if dt > 1 else timer[1]

                if firstTick:
                    firstTick = False
                    minute, seconds = timer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    timer[0] = timer[0] - 1 if timer[0] > 1 and timer[1] == 0 else (0 if timer[0] == 0 else timer[0])
                    timer[1] = 59 if timer[1] == 0 else timer[1] - 1
                    lastTime = time.time()

                elif time.time() - lastTime >= 1:
                    if timer[0] == 0 and timer[1] == -1:
                        minute, seconds = timer
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                        screen.blit(timeText, (timeWidth, timeHeight))
                        
                        pygame.mixer.music.load(working_dir + r"assets\sound_effects\argon.mp3")
                        pygame.mixer.music.play(5)
                        screen.fill(BG)
                        finishedText = subheader_font_medium.render("Session Completed!", False, BLACK)
                        fade((finishedText,  (width - 725, height - 300)))
                        pygame.time.delay(1500)
                        firstTick = True
                        timer = [30, 0]
                        status = "break"
                    else:
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                        screen.blit(timeText, (timeWidth, timeHeight))

                        minute, seconds = timer
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                        screen.blit(timeText, (timeWidth, timeHeight))
                        timer[1] = timer[1] - 1
                        lastTime = time.time()

                        if timer[0] != 0 and timer[1] == -1:
                            timer[0] -= 1
                            timer[1] = 59
            
            case "break":
                rectCoordinates = (318, 218, 150, 20)
                textCoordinates = (340, 220)

                if not breakScreenFaded:
                    displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin Break?", BLACK, textCoordinates, True)))
                    breakScreenFaded = True

                elif 318 <= mouse[0] <= 468 and 218 <= mouse[1] <= 238:
                    displayButton(b = ((DARK_GREY, rectCoordinates), (button_font, "Begin Break?", WHITE, textCoordinates, False)))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(button_select)

                        buttonBG = pygame.Surface((150, 20))
                        headerBG = pygame.Surface((750, 60))
                        buttonBG.fill(BG)
                        headerBG.fill(BG)
                        
                        displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin the chill!", BLACK, textCoordinates, False)))
                        fade((buttonBG, (318, 218)), (headerBG, (30, 145)))

                        status = "break_timer"
                else:
                    displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin Break?", BLACK, textCoordinates, False)))
            
            case "break_timer":
                dt = time.time() - iTime
                breakTimer[1] = breakTimer[1] - int(dt) if dt > 1 else breakTimer[1]

                if firstTick:
                    firstTick = False
                    minute, seconds = breakTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    breakTimer[0] = breakTimer[0] - 1 if breakTimer[0] > 1 and breakTimer[1] == 0 else(0 if breakTimer[0] == 0 else breakTimer[0])
                    breakTimer[1] = 59 if breakTimer[1] == 0 else breakTimer[1] - 1
                    lastTime = time.time()
                elif time.time() - lastTime >= 0.980:
                    if breakTimer[0] == 0 and breakTimer[1] == -1:
                        minute, seconds = breakTimer
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                        screen.blit(timeText, (timeWidth, timeHeight))
                        
                        pygame.mixer.music.load(working_dir + r"assets\sound_effects\argon.mp3")
                        pygame.mixer.music.play(5)
                        screen.fill(BG)
                        firstTick = True
                        breakTimer = [5, 0]
                        status = "end"
                    else:
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                        screen.blit(timeText, (timeWidth, timeHeight))

                        minute, seconds = breakTimer
                        timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                        screen.blit(timeText, (timeWidth, timeHeight))
                        breakTimer[1] = breakTimer[1] - 1
                        lastTime = time.time()

                        if breakTimer[0] != 0 and breakTimer[1] == -1:
                            breakTimer[0] -= 1
                            breakTimer[1] = 59

            case "end":
                rectCoordinates_Button1 = (200, 245, 130, 20)
                textCoordinates_Button1 = (210, 247)

                rectCoordinates_Button2 = (500, 245, 70, 20)
                textCoordinates_Button2 = (515, 247)

                screenDummy = pygame.Surface((width, height))
                screenDummy.fill(BG)

                endFont1 = subheader_font_small.render("Pomodoro Session", False, BLACK)
                endFont2 = subheader_font_large.render("Complete!", False, BLACK)

                if not endScreenFaded:

                    fade((endFont1, (160, 100)), (endFont2, (140, 130)))
                    displayButton(b1 = ((GREY, rectCoordinates_Button1), (button_font, "Home Screen?", BLACK, textCoordinates_Button1, True)), b2 = ((GREY, rectCoordinates_Button2), (button_font, "Quit?", BLACK, textCoordinates_Button2, True)))
                    
                    endScreenFaded = True

                elif 200 <= mouse[0] <= 330 and 245 <= mouse[1] <= 265:
                    displayButton(b = ((DARK_GREY, rectCoordinates_Button1), (button_font, "Home Screen?", WHITE, textCoordinates_Button1, False)))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.Sound.play(button_select)

                        startScreenFade = False
                        breakScreenFade = False
                        endScreenFade = False
                        status = "begin"

                        fade((screenDummy, (0,0)))

                        pygame.mixer.music.stop()

                elif 500 <= mouse[0] <= 570 and 245 <= mouse[1] <= 265:
                    displayButton(b  =((DARK_GREY, rectCoordinates_Button2),(button_font, "Quit?", WHITE, textCoordinates_Button2, False)))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(button_select)

                        fade((screenDummy, (0, 0)))
                        pygame.time.delay(500)
                        running = False
                else:
                    displayButton(b1 = ((GREY, rectCoordinates_Button1), (button_font, "Home Screen?", BLACK, textCoordinates_Button1, False)), b2 = ((GREY, rectCoordinates_Button2), (button_font, "Quit?", BLACK, textCoordinates_Button2, False)))      
pygame.quit()