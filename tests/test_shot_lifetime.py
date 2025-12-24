import pygame
import unittest
from shot import Shot
import wrap_patch
import shot_patch

class TestShotLifetime(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        Shot.containers = (self.updatable, self.drawable)

    def tearDown(self):
        pygame.quit()

    def test_shot_expires_after_lifetime(self):
        s = Shot(0, 0)
        s.lifetime = 0.2
        # simulate multiple small updates
        s.update(0.1)
        self.assertTrue(s.alive())
        s.update(0.15)
        self.assertFalse(s.alive())

if __name__ == '__main__':
    unittest.main()
