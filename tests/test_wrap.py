import pygame
import unittest
# ensure monkey-patches are applied for wrap behavior
import wrap_patch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteroid import Asteroid
from player import Player
from shot import Shot

class TestWrap(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_asteroid_wraps(self):
        a = Asteroid(-10, -20, 30)
        a.velocity = pygame.Vector2(0, 0)
        a.update(0.0)
        self.assertTrue(0 <= a.position.x < SCREEN_WIDTH)
        self.assertTrue(0 <= a.position.y < SCREEN_HEIGHT)

    def test_shot_wraps(self):
        s = Shot(SCREEN_WIDTH + 5, SCREEN_HEIGHT + 5)
        s.velocity = pygame.Vector2(0, 0)
        s.update(0.0)
        self.assertTrue(0 <= s.position.x < SCREEN_WIDTH)
        self.assertTrue(0 <= s.position.y < SCREEN_HEIGHT)

    def test_player_wraps(self):
        p = Player(SCREEN_WIDTH + 100, -50)
        p.move(0)
        self.assertTrue(0 <= p.position.x < SCREEN_WIDTH)
        self.assertTrue(0 <= p.position.y < SCREEN_HEIGHT)

if __name__ == '__main__':
    unittest.main()
