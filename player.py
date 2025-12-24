import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

# Player class representing the player's spaceship
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0.0
        self.lives = PLAYER_LIVES

    def respawn(self):
        """Reset position and state for a respawn."""
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        # reset shoot cooldown so player can react immediately
        self.shoot_cooldown_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(
            screen, 
            "white", 
            self.triangle(), 
            LINE_WIDTH
        )
    
    def rotate(self, dt):
        # adjust rotation based on turn speed and delta time
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        """Apply acceleration in the facing direction. If dt is negative, apply reverse acceleration."""
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        # dt acts as a signed scalar here (positive to accelerate forward)
        self.velocity += forward * (PLAYER_ACCELERATION * dt)
        # clamp to max speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def shoot(self, dt):
        if self.shoot_cooldown_timer > 0:
            return
        self.shoot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

        # integrate velocity into position
        self.position += self.velocity * dt

        # simple linear drag to slowly reduce velocity when not accelerating
        drag_factor = max(0.0, 1.0 - PLAYER_DRAG * dt)
        self.velocity *= drag_factor

        # wrap player around screen if necessary
        try:
            self.wrap_around()
        except Exception:
            pass

        # decrease shoot cooldown timer
        self.shoot_cooldown_timer = max(0.0, self.shoot_cooldown_timer - dt)





