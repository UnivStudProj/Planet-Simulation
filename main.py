# Idead source:
# https://www.youtube.com/watch?v=WTLPmUHTPqo

import pygame
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
        self.sunLine = []
        
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
                
        # Sun moving illusion
        else:
            # Filling an empty list
            if not self.sunLine:
                self.sunLine.append((x, y))
                self.sunLine.append((x, y + self.radius))
            # Draw line if it not off the screen
            elif not self.sunLine[-1][1] > HEIGHT:
                self.sunLine.append((x, self.sunLine[-1][1] + 0.1))
            
            pygame.draw.lines(WIN, self.color, False, self.sunLine, 2)
    
    def attraction(self, other):
        # Other planet coords
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y 
        distance = np.sqrt(distance_x **2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = np.arctan2(distance_y, distance_x)
        force_x = np.cos(theta) * force
        force_y = np.sin(theta) * force
        
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


class Star:
    
    def __init__(self, amount, color, offset, size):
        self.amount = amount
        self.color = color
        self.offset = offset
        self.size = size 
        self.field = self.setField(self.amount)
        
    @staticmethod 
    def setField(amount):
        field = np.empty((amount, 2), dtype=int)
        for i in range(0, np.shape(field)[0]):
            x = np.random.randint(0, WIDTH)
            y = np.random.randint(0, HEIGHT)
            field[i] = [x, y]
        
        return field
        
    def draw(self):
        for star in self.field:
            if star[1] > HEIGHT:
                star[0] = np.random.randint(0, WIDTH)
                star[1] = -1
            star[1] += self.offset
            
            pygame.draw.circle(WIN, self.color, star, self.size)
        

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
    
    star_slow = Star(30, '#b5179e', 1, 1)
    star_medium = Star(20, '#480ca8', 4, 2)
    star_fast = Star(10, '#4cc9f0', 8, 3)
    
    stars = [star_slow, star_medium, star_fast]
    
    while run:
        clock.tick(75) # 75 fps
        WIN.fill('#02010E')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for star in stars:
            star.draw() 
         
        for planet in planets:
            planet.update_position(planets)
            planet.draw()

            
        pygame.display.update()
    
    pygame.quit()
    
if __name__ == '__main__':
    main()