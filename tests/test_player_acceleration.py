import pygame
import unittest
from player import Player
from constants import PLAYER_ACCELERATION, PLAYER_MAX_SPEED

class TestPlayerAcceleration(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_accelerates_forward(self):
        p = Player(100, 100)
        self.assertEqual(p.velocity.length(), 0)
        p.move(0.1)
        self.assertGreater(p.velocity.length(), 0)

    def test_max_speed_clamped(self):
        p = Player(0,0)
        # apply acceleration repeatedly
        for _ in range(100):
            p.move(0.1)
        self.assertLessEqual(p.velocity.length(), PLAYER_MAX_SPEED + 1e-6)

    def test_drag_slows_down(self):
        p = Player(0,0)
        p.move(0.5)
        speed_after_accel = p.velocity.length()
        p.update(1.0)
        self.assertLess(p.velocity.length(), speed_after_accel)

if __name__ == '__main__':
    unittest.main()
