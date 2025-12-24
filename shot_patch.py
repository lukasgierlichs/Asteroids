from shot import Shot
from constants import SHOT_LIFETIME_SECONDS

_orig_shot_update = Shot.update

def _shot_update(self, dt):
    # ensure lifetime exists for shots created before this patch
    if not hasattr(self, "lifetime"):
        self.lifetime = SHOT_LIFETIME_SECONDS

    # call original update (moves position)
    _orig_shot_update(self, dt)

    # decrease lifetime and kill when expired
    self.lifetime -= dt
    if self.lifetime <= 0:
        self.kill()
        return

    # attempt to wrap; wrap_patch may already handle this, but do it here for safety
    try:
        self.wrap_around()
    except Exception:
        pass

Shot.update = _shot_update
