import pygame
import time
import unittest
from explosion import Explosion

class TestExplosion(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_explosion_lifetime(self):
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        Explosion.containers = (updatable, drawable)
        e = Explosion(0, 0, max_radius=20, duration=0.2)
        # sprite should be in a group on creation
        self.assertTrue(e.alive())
        e.update(0.1)
        self.assertTrue(e.alive())
        e.update(0.2)
        self.assertFalse(e.alive())

if __name__ == '__main__':
    unittest.main()
