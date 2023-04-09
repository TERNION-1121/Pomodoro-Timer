from init_and_funcs import *

# main loop
while running:  
    iTime = time.time()
    for event in pygame.event.get():    # event loop
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
            dt = int(time.time() - iTime)
            mainTimer[1] = mainTimer[1] - dt if dt > 1 and dt <= mainTimer[1] else (-1 if dt > mainTimer[1] else mainTimer[1])
            
            if firstTick:
                minute, seconds = mainTimer
                timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                screen.blit(timeText, (timeWidth, timeHeight))
                
                mainTimer[0] = mainTimer[0] - 1 if mainTimer[0] > 1 and mainTimer[1] == 0 else (0 if mainTimer[0] == 0 else mainTimer[0])
                mainTimer[1] = 59 if mainTimer[1] == 0 else mainTimer[1] - 1

                firstTick = False
                lastTime = time.time()

            elif time.time() - lastTime >= 0.990:
                if mainTimer[0] == 0 and mainTimer[1] == -1:
                    minute, seconds = mainTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    screen.fill(BG)

                    pygame.mixer.music.load(working_dir + r"assets\sound_effects\argon.mp3")
                    pygame.mixer.music.play(5)

                    firstTick = True
                    mainTimer = [30, 0]
                    totalSessionPeriod += mainTimer[0]
                    status = "big_break" if totalSessionPeriod >= 120 else "break"
                else:
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                    screen.blit(timeText, (timeWidth, timeHeight))

                    minute, seconds = mainTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    
                    mainTimer[1] = mainTimer[1] - 1
                    lastTime = time.time()

                    if mainTimer[0] != 0 and mainTimer[1] == -1:
                            mainTimer[0] -= 1
                            mainTimer[1] = 59
            
        case "break":
            rectCoordinates = (318, 218, 150, 20)
            textCoordinates = (340, 220)

            if not breakScreenFaded:
                finishedText = subheader_font_medium.render("Session Completed!", False, BLACK)
                fade((finishedText,  (width - 725, height - 300)))
                pygame.time.delay(1500)
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
            dt = int(time.time() - iTime)
            breakTimer[1] = breakTimer[1] - dt if dt > 1 and dt <= breakTimer[1] else (-1 if dt > breakTimer[1] else breakTimer[1])

            if firstTick:
                firstTick = False
                minute, seconds = breakTimer
                timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                screen.blit(timeText, (timeWidth, timeHeight))
                breakTimer[0] = breakTimer[0] - 1 if breakTimer[0] > 1 and breakTimer[1] == 0 else(0 if breakTimer[0] == 0 else breakTimer[0])
                breakTimer[1] = 59 if breakTimer[1] == 0 else breakTimer[1] - 1
                lastTime = time.time()
            elif time.time() - lastTime >= 0.990:
                if breakTimer[0] == 0 and breakTimer[1] == -1:
                    minute, seconds = breakTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    screen.fill(BG)
                        
                    pygame.mixer.music.load(working_dir + r"assets\sound_effects\argon.mp3")
                    pygame.mixer.music.play(5)

                    firstTick = True
                    breakTimer = [5, 0]
                    totalSessionPeriod += breakTimer[0] + 120
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

        case "big_break":

            rectCoordinates = (318, 248, 164, 20)
            textCoordinates = (324, 250)

            if not bigBreakScreenFaded:
                workedBigFont = subheader_font_medium.render("You worked ", False, BLACK)
                breakBigFont  = basic_font.render("So have a break that's", False, BLACK)
                bigFont       = bold_font.render("BIG!", False, BLACK)
                fade((workedBigFont, (20, 120)), (breakBigFont, (30, 192)), (bigFont, (420, 90)))

                displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin the Big Break?", BLACK, textCoordinates, True)))
                bigBreakScreenFaded = True

            elif 318 <= mouse[0] <= 482 and 248 <= mouse[1] <= 268:
                displayButton(b = ((DARK_GREY, rectCoordinates), (button_font, "Begin the Big Break?", WHITE, textCoordinates, False)))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(button_select)

                    buttonBG = pygame.Surface((180, 30))
                    headerBG = pygame.Surface((750, 120))
                    buttonBG.fill(BG)
                    headerBG.fill(BG)
                        
                    displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin the BIG CHILL!", BLACK, textCoordinates, False)))
                    fade((buttonBG, (318, 248)), (headerBG, (24, 120)))

                    status = "big_break_timer"
            else:
                displayButton(b = ((GREY, rectCoordinates), (button_font, "Begin the Big Break?", BLACK, textCoordinates, False)))

        case "big_break_timer":
            dt = int(time.time() - iTime)
            bigBreakTimer[1] = bigBreakTimer[1] - dt if dt > 1 and dt <= bigBreakTimer[1] else (-1 if dt > bigBreakTimer[1] else bigBreakTimer[1])

            if firstTick:
                firstTick = False
                minute, seconds = bigBreakTimer
                timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                screen.blit(timeText, (timeWidth, timeHeight))
                bigBreakTimer[0] = bigBreakTimer[0] - 1 if bigBreakTimer[0] > 1 and bigBreakTimer[1] == 0 else(0 if bigBreakTimer[0] == 0 else bigBreakTimer[0])
                bigBreakTimer[1] = 59 if bigBreakTimer[1] == 0 else bigBreakTimer[1] - 1
                lastTime = time.time()
            elif time.time() - lastTime >= 0.990:
                if bigBreakTimer[0] == 0 and bigBreakTimer[1] == -1:
                    minute, seconds = bigBreakTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    screen.fill(BG)
                        
                    pygame.mixer.music.load(working_dir + r"assets\sound_effects\argon.mp3")
                    pygame.mixer.music.play(5)

                    firstTick = True
                    bigBreakTimer = [20, 0]
                    totalSessionPeriod = 0
                    status = "end"
                else:
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BG)
                    screen.blit(timeText, (timeWidth, timeHeight))

                    minute, seconds = bigBreakTimer
                    timeText = timer_font.render(f"{minute:02d}:{seconds:02d}", False, BLACK)
                    screen.blit(timeText, (timeWidth, timeHeight))
                    bigBreakTimer[1] = bigBreakTimer[1] - 1
                    lastTime = time.time()

                    if bigBreakTimer[0] != 0 and bigBreakTimer[1] == -1:
                        bigBreakTimer[0] -= 1
                        bigBreakTimer[1] = 59
        
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
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(button_select)

                    startScreenFaded = False
                    breakScreenFaded = False
                    endScreenFaded = False
                    status = "begin"

                    fade((screenDummy, (0,0)))


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