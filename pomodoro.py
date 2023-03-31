import pygame

def fade_text(text, screen, coord):
        for alpha in range(50):
            text.set_alpha(alpha)
            screen.blit(text, coord)
            pygame.display.flip()
            pygame.time.delay(30)

# basic initilizations/setup
pygame.init()
pygame.font.init()
width, height = 768, 432
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# background and colors
BG = (223, 235, 247) 
BLACK = (0, 0, 0)
GREY = (200, 210, 224)
screen.fill(BG)
pygame.display.flip()

# font setup
header_font = pygame.font.Font('E:\static\LexendGiga-Regular.ttf', 40)
button_font = pygame.font.Font('E:\static\LexendGiga-Thin.ttf')

mainFont = header_font.render("Pomodoro Timer", False, BLACK)
mainFont.set_alpha(0)
readyFont = button_font.render("Ready?", False, BLACK)
beginFont = button_font.render("Begin!", False, BLACK)

fade_text(mainFont, screen, (192, 127))
pygame.draw.rect(screen, GREY, ((width // 2) - 10, 198, 70, 20))
fade_text(readyFont, screen, (width // 2, 200))
pygame.display.flip()
# event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (width // 2) <= mouse[0] <= (width // 2) + 70 and 198 <= mouse[1] <= 218:
                pygame.draw.rect(screen, GREY, ((width // 2) - 10, 198, 70, 20))
                fade_text(beginFont, screen, (width // 2, 200))
                
pygame.quit()
