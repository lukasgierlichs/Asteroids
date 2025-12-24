# Monkey-patch movement/update methods to apply screen wrap-around
from player import Player
from asteroid import Asteroid
from shot import Shot

# Patch Player.move to call wrap_around after moving
_orig_player_move = Player.move
def _player_move(self, dt):
    _orig_player_move(self, dt)
    self.wrap_around()
Player.move = _player_move

# Patch Asteroid.update to call wrap_around after update
_orig_asteroid_update = Asteroid.update
def _asteroid_update(self, dt):
    _orig_asteroid_update(self, dt)
    self.wrap_around()
Asteroid.update = _asteroid_update

# Patch Shot.update to call wrap_around after update
_orig_shot_update = Shot.update
def _shot_update(self, dt):
    _orig_shot_update(self, dt)
    self.wrap_around()
Shot.update = _shot_update
