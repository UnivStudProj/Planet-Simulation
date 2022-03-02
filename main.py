# Idead source:
# https://www.youtube.com/watch?v=WTLPmUHTPqo

from tracemalloc import start
import pygame
import math
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 800
FONT = pygame.font.SysFont('Arial', 19)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

class Planet:
    # Astronomical unit (distance between sun and earth)
    # Converting from kilometers to meters multiplying by 1000
    AU = 149.6e6 * 1000
    
    # Gravitational constant
    G = 6.67428e-11
   
    # 1 AU = 100 pixels
    # Lower => less distance between planets
    SCALE = 200 / AU
    
    # time pass per 1 frame 
    TIMESTEP = 3600 * 12

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        # Let it be just as an exception...
        self.sun = False
        self.orbit = []
        self.distance_to_sun = 0
        
        # Velocity 
        self.x_vel = 0
        self.y_vel = 0
        
        # Trail making parameters
        self.x0 = x * self.SCALE + WIDTH / 2
        self.y0 = y * self.SCALE + HEIGHT / 2
        self.erase = False
        
    def draw(self):
        # Scaling coordinates and 
        # adding the offset to move from the top left corner
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
         
        # Drawing orbits
        if len(self.orbit) > 1: 
            update_points = []
            for point in self.orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.SCALE + WIDTH / 2
                orbit_y = orbit_y * self.SCALE + HEIGHT / 2
                update_points.append((orbit_x, orbit_y))

            pygame.draw.lines(WIN, self.color, False, update_points, 2)
           
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)
        
        # Distance text 
        if not self.sun:
            distance_text = FONT.render(f'{self.distance_to_sun / 1000:,.0f} km', 1, 'white')
            text_offset = distance_text.get_width() / 2
            WIN.blit(distance_text, (x - text_offset, y - text_offset))
           
            # defining at what 'y' erase starts 
            erase_y = self.y0 - 1 <= int(y) <= self.y0 + 1
            if self.erase:
                self.orbit.pop(0)
            # adding length condition to escape erasing at the beginning
            elif erase_y and len(self.orbit) > 5:
                self.erase = True
    
    def attraction(self, other):
        # Other planet coords
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y 
        distance = math.sqrt(distance_x **2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    def update_position(self, planets):
        if not self.sun:
            total_fx = total_fy = 0
            for planet in planets:
                if self == planet:
                    continue
                
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy
                
            self.x_vel += total_fx / self.mass * self.TIMESTEP
            self.y_vel += total_fy / self.mass * self.TIMESTEP
            
            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))


class Stars:
    SLOW_OFFSET = 0.1
    MEDIUM_OFFSET = 0.2
    FAST_OFFSET = 0.3
    STARS_COLORS = [
        '#f72585', '#b5179e', '#7209b7', '#560BAD', '#480CA8',
        '#3A0CA3', '#3F37C9', '#4361EE', '#4895EF', '#4CC9F0',
    ]
    
    def __init__(self, *starsAmount):
        self.__slowStars = starsAmount[0]
        self.__mediumStars = starsAmount[1]
        self.__fastStars = starsAmount[2]
    
        self.slowField = np.array(self.setField(self.__slowStars), dtype=float)
        self.mediumField = np.array(self.setField(self.__mediumStars), dtype=float)
        self.fastField = np.array(self.setField(self.__fastStars), dtype=float)
    
    @staticmethod 
    def setField(starsType):
        starX = np.random.uniform(0, WIDTH, size=(starsType))
        starY = np.random.uniform(0, HEIGHT, size=(starsType))
        
        return (starX, starY)
    
    def drawStars(self):
        slow = self.checkHeightPos(self.slowField, self.SLOW_OFFSET) 
        medium = self.checkHeightPos(self.mediumField, self.MEDIUM_OFFSET) 
        fast = self.checkHeightPos(self.fastField, self.FAST_OFFSET)
        
        self.drawing(slow) 
        self.drawing(medium) 
        self.drawing(fast) 
    
    def drawing(self, star):
        color = self.STARS_COLORS[np.random.randint(0, len(self.STARS_COLORS))]
        for x, y in zip(star[0], star[1]):
            pygame.draw.circle(WIN, color, (x, y), np.random.randint(1, 4))
        
    
    @staticmethod
    def checkHeightPos(star, starOffset):
        for y in star[1]:
            curr_index = list(star[1]).index(y)
            star[1][curr_index] += starOffset
            if y > HEIGHT:
                # current 'y'
                star[1][curr_index] = -1
                # current 'x'
                star[0][curr_index] = np.random.randint(0, WIDTH)
                
        return star 
        

def main():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, 'yellow', 1.98892e30)
    sun.sun = True
    
    # 'y' velocity should be postive if 'AU' is negative and vice versa 
    earth = Planet(-1 * Planet.AU, 0, 16, 'lightblue', 5.9742e24)
    earth.y_vel = 29.783e3
    
    mars = Planet(-1.524 * Planet.AU, 0, 12, 'darkred', 6.39e23)
    mars.y_vel = 24.077e3
    
    mercury = Planet(0.387 * Planet.AU, 0, 8, 'darkgrey', 3.30e23)
    mercury.y_vel = -47.4e3
    
    venus = Planet(0.723 * Planet.AU, 0, 14, 'orange', 4.8685e24)
    venus.y_vel = -35.02e3
    
    planets = [sun, earth, mars, mercury, venus]
    
    star = Stars(25, 15, 5)
    
    while run:
        clock.tick(75) # 75 fps
        WIN.fill('#02010E')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            star.drawStars()
            planet.draw()

            
        pygame.display.update()
    
    pygame.quit()
    
if __name__ == '__main__':
    main()