
import pygame
import random
import sys
import math
from recorder import startRecord, stopRecord, disconnect

# Record perm
RecordingEnabled = True
if len(sys.argv) > 1 and sys.argv[1] == "norecord":
    RecordingEnabled = False
    print("OBS recording disabled")
else:
    print("OBS recording enabled")

# Global stuff
TITLE = "Pygame Test"
SCREEN_RATIO = 0.3
SCREEN_WIDTH, SCREEN_HEIGHT = 1080 * SCREEN_RATIO, 1920 * SCREEN_RATIO
BACKGROUND = (0,0,0)

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption(TITLE)
dt = 0

# Entity Setup

PERSON_COUNT = 100

persons = []
class Person():
    size = [25, 25]
    color = [255, 0, 0]
    speed = 0.2
    attackSpeed = 15
    
    parent = persons
    def __init__(self):
        self.position = [random.randint(0, int(SCREEN_WIDTH)),  random.randint(0, int(SCREEN_HEIGHT))]
        self.velocity = [0, 0]
        self.health = 10
        self.damage = 1
        self.target = False
        self.tick = 0
        
    def update(self):
        
        self.tick += 1
        
        # Find target
        if not self.target or self.target.health <= 0:
            maxDist = 999999
            for p in self.parent:
                if p == self:
                    continue
                dist = math.sqrt((self.position[0] - p.position[0]) ** 2 + (self.position[1] - p.position[1]) ** 2)
                if dist < maxDist:
                    maxDist = dist
                    self.target = p
        
        # Move towards target
        if self.target:
            xd, yd = self.target.position[0] - self.position[0], self.target.position[1] - self.position[1]
            dist = math.sqrt(xd ** 2 + yd ** 2)
            
            if dist > 20:
                dir = math.atan2(yd, xd)
                xv, yv = math.cos(dir) * self.speed, math.sin(dir) * self.speed
                self.velocity[0] += xv
                self.velocity[1] += yv
            elif self.tick % self.attackSpeed == 0:
                self.target.takeDamage(self.damage)
                
        # Move
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Dampen velocity
        self.velocity[0] *= 0.85
        self.velocity[1] *= 0.85
        
        # Death
        if self.health <= 0:
            self.parent.remove(self)
            
    def draw(self):
        w, h = self.size
        x, y = self.position[0] - w / 2, self.position[1] - h / 2
        pygame.draw.rect(screen, self.color, (x, y, w, h))
        
    def takeDamage(self,amount=0):
        self.health -= amount

# Game Loop

def init():
    for i in range(PERSON_COUNT):
        persons.append(Person())

def update():
    for p in persons:
        p.update()
    
    
def draw():
    for p in persons:
        p.draw()

init()

if RecordingEnabled:
    startRecord()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if RecordingEnabled:
                stopRecord()
                disconnect()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            if RecordingEnabled:
                stopRecord()
                disconnect()
            
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
            
    screen.fill(BACKGROUND)
    update()
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()