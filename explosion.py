import pygame
from circleshape import CircleShape
from constants import EXPLOSION_MAX_RADIUS, EXPLOSION_DURATION

class Explosion(CircleShape):
    def __init__(self, x, y, max_radius=None, duration=None, color=(255, 160, 0)):
        max_radius = max_radius or EXPLOSION_MAX_RADIUS
        duration = duration or EXPLOSION_DURATION
        super().__init__(x, y, 1)
        self.max_radius = max_radius
        self.duration = duration
        self.elapsed = 0.0
        self.color = color

    def update(self, dt):
        self.elapsed += dt
        t = self.elapsed / self.duration
        if t >= 1.0:
            self.kill()
            return
        self.radius = self.max_radius * t

    def draw(self, screen):
        # Draw a fading filled circle onto a surface with per-pixel alpha
        size = int(self.max_radius * 2) + 4
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        t = min(1.0, max(0.0, self.elapsed / self.duration))
        alpha = max(0, 255 - int(255 * t))
        r = max(1, int(self.radius))
        col = (*self.color[:3], alpha)
        pygame.draw.circle(surf, col, (size // 2, size // 2), r)
        pos = (int(self.position.x - size // 2), int(self.position.y - size // 2))
        screen.blit(surf, pos)
