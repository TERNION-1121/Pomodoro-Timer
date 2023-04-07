import time
from random import random
import pygame
from os import system
frameRate = 200
dt = 1/200
FoNt = 0
FoNtprint = 0
GREEN = (25, 187, 86)
lightGREEN = (25-10, 187-30, 86-20)
class sphere:
    def __init__(self, position : list, radius : float, velocity, number : int, color : list):
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.radius = radius
        self.vel = pygame.math.Vector2(velocity[0], velocity[1])
        self.n = number
        self.color = color
    
    def update(self, dt):

        if self.vel.magnitude() > 20:
            self.vel = pygame.math.Vector2(20).rotate(pygame.math.Vector2(20).angle_to(self.vel))

        if self.pos[0] > 790:
            self.pos[0] = 789
            self.vel[0] = -self.vel[0]
        elif self.pos[0] < 10:
            self.pos[0] = 11
            self.vel[0] = -self.vel[0]
        
        if self.pos[1] > 790:
            self.pos[1] = 789
            self.vel[1] = -self.vel[1]
        elif self.pos[1] < 10:
            self.pos[1] = 11
            self.vel[1] = -self.vel[1]

        self.pos += self.vel*dt

    def is_colliding(obj1, obj2):
        return True if (sphere.distance(obj1.pos, obj2.pos) < obj1.radius + obj2.radius) else False

    def distance(point1 : list, point2 : list):
        if min([len(point1), len(point2)]) == 2:
            return ((((point1[0]-point2[0])**2) + ((point1[1] - point2[1])**2))**0.5)
        
        else:
            return ((((point1[0]-point2[0])**2) + ((point1[1] - point2[1])**2) + ((point1[2] - point2[2])**2))**0.5)

def cls():
    system("cls")
def font(a:str,b=18):
    global FoNt
    FoNt = pygame.font.SysFont(a,b)
def printpy(x:str,a=(100,400),y=(128,128,128)):
    global FoNt,FoNtprint
    FoNtprint = FoNt.render(x,True,y)
    screen.blit(FoNtprint,a)
pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Random Geometrical Patterns")
cls()
OBJS = list()
for _ in range(75):
    OBJS.append( sphere([random()*800, random()*800], random()*120, [(0.5-random())*2, (0.5-random())*2], _, [random()*256, random()*256, random()*256]) )
running = True
clock = pygame.time.Clock()
rectangle = pygame.Surface((800, 800))
rectangle.set_alpha(5)
rectangle.fill((0, 0, 0))
while running == True:
    clock.tick(frameRate)
    initTime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(rectangle, (0, 0))

    for circle in OBJS:
        for circle2 in OBJS:
            if circle.n != circle2.n:
                if sphere.is_colliding(circle, circle2):
                    pygame.draw.line(screen, [(circle.color[0]+circle2.color[0])/2, (circle.color[1]+circle2.color[1])/2, (circle.color[2]+circle2.color[2])/2], circle.pos[:2], circle2.pos[:2])
                    pygame.draw.circle(screen, circle.color, circle.pos[:2], 2)
                    pygame.draw.circle(screen, circle2.color, circle2.pos[:2], 2)

        circle.vel[0] += (0.5-random())*90*dt
        circle.vel[1] += (0.5-random())*90*dt
    
        circle.update(dt)
    pygame.display.update()
    endTime = time.time()
    dt = endTime-initTime
    if dt != 0:
        frameRate = 1/dt
    else:
        frameRate = 1000