import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH,
        )
    
    def split(self):
        # If asteroid is too small, just remove it
        if self.radius <= ASTEROID_MIN_RADIUS:
            log_event("asteroid_destroyed")
            self.kill()
            return

        # Create two smaller asteroids
        old_radius = self.radius
        new_radius = old_radius - ASTEROID_MIN_RADIUS
        log_event("asteroid_split")

        # spawn new asteroids at roughly the same position
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        # determine split angles and velocities
        angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(angle)
        v2 = self.velocity.rotate(-angle)

        # if original was stationary, give them a small random push
        if v1.length() == 0:
            v1 = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 50
        if v2.length() == 0:
            v2 = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 50

        # add slight random speed variation
        v1 = v1 * random.uniform(0.8, 1.2)
        v2 = v2 * random.uniform(0.8, 1.2)

        a1.velocity = v1
        a2.velocity = v2

        # nudge positions a little so they don't perfectly overlap
        try:
            a1.position = self.position + v1.normalize() * (new_radius * 0.5)
            a2.position = self.position + v2.normalize() * (new_radius * 0.5)
        except ValueError:
            # fallback if normalization fails
            a1.position = self.position
            a2.position = self.position

        # remove the original asteroid
        self.kill()


    def update(self, dt):
        self.position += self.velocity * dt