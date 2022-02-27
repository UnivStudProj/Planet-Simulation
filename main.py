import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

class Planet:
    # Astronomical unit (distance between sun and earth)
    # Converting from kilometers to meters multiplying by 1000
    AU = 149.6e6 * 1000
    
    # Gravitational constant
    G = 6.67428e-11
   
    # 1 AU = 100 pixels 
    SCALE = 250 / AU
    
    # 1 day per 1 frame 
    TIMESTEP = 3600 * 24
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = [] 
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        # Scaling coordinates and setting the offset from the center
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)


def main():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60) # 60 fps
        # WIN.fill('#02010E')
        # pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()
    

main()