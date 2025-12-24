import os
import tempfile
import json
import unittest
import leaderboard

class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        # use a temp file to avoid touching real leaderboard
        self.tmpdir = tempfile.TemporaryDirectory()
        self.orig_path = leaderboard.FILE_PATH
        leaderboard.FILE_PATH = os.path.join(self.tmpdir.name, "lb.json")

    def tearDown(self):
        leaderboard.FILE_PATH = self.orig_path
        self.tmpdir.cleanup()

    def test_add_and_get_top(self):
        leaderboard.add_score("Alice", 100)
        leaderboard.add_score("Bob", 200)
        leaderboard.add_score("Carol", 150)
        top = leaderboard.get_top(3)
        scores = [e['score'] for e in top]
        self.assertEqual(scores, [200, 150, 100])

    def test_limit_entries(self):
        for i in range(15):
            leaderboard.add_score(f"P{i}", i * 10)
        top = leaderboard.get_top(10)
        self.assertEqual(len(top), 10)
        self.assertEqual(top[0]['score'], 140)

if __name__ == '__main__':
    unittest.main()
