
import pygame
import random

TITLE = "Pygame Test"
SCREEN_RATIO = 0.3
SCREEN_WIDTH, SCREEN_HEIGHT = 1080 * SCREEN_RATIO, 1920 * SCREEN_RATIO
BACKGROUND = (0,0,0)

# pygame setup
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption(TITLE)

persons = []
    
class Person():
    size = [25, 25]
    color = [255, 0, 0]
    parent = persons
    def __init__(self):
        self.position = [random.randint(0, int(SCREEN_WIDTH)),  random.randint(0, int(SCREEN_HEIGHT))]
        self.velocity = [0, 0]
        self.health = 100
        
    def update(self,i):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.health -= 1
        
        if self.health < 0:
            self.parent.remove(i)
        
    
    def draw(self):
        w, h = self.size
        x, y = self.position[0] - w / 2, self.position[1] - h / 2
        pygame.draw.rect(screen, self.color, (x, y, w, h))

def init():
    
    for i in range(10):
        persons.add(Person())
    

def update():
    for p in persons:
        p.update()
    
    
def draw():
    for p in persons:
        p.draw()

init()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    screen.fill(BACKGROUND)
    update()
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()