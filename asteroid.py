import pygame
import random
import math
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(50, 100)
        self.shape = self.generate_lumpy_shape()  # Generate shape only once during initialization
    
    def generate_lumpy_shape(self):
        points = []
        num_points = random.randint(8, 12)
        for i in range(num_points):
            angle = (2 * math.pi / num_points) * i
            offset = random.uniform(0.7, 1.3)  # Controls how lumpy the asteroid is
            r = self.radius * offset
            x = math.cos(angle) * r
            y = math.sin(angle) * r
            points.append((x, y))  # Relative to center
        return points

    def draw(self, screen):
        translated_points = [
            (self.position.x + x, self.position.y + y) for (x, y) in self.shape
        ]
        pygame.draw.polygon(screen, "white", translated_points, 2)
    
    def update(self, dt):
        # Only update the position, don't regenerate shape here
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        for velocity in [velocity1, velocity2]:
            new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid.velocity = velocity * 1.2
            # Don't regenerate shape again, as it's already done
            new_asteroid.shape = new_asteroid.generate_lumpy_shape()  
            Asteroid.containers[0].add(new_asteroid)

