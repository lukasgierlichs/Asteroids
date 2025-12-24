import pygame
import sys
import math
import time
from constants import *
from logger import log_state
from logger import log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
# ensure wrap behavior is enabled
import wrap_patch

def main():
    pygame.init()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # simple HUD font
    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    # ask for player name before creating the player
    player_name = "Player"
    def ask_player_name(screen, font):
        name = ""
        clock = pygame.time.Clock()
        prompt = "Enter name (press Enter): "
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name.strip() or "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 20 and event.unicode.isprintable():
                            name += event.unicode
            screen.fill("black")
            txt = font.render(prompt + name, True, "white")
            screen.blit(txt, (50, 200))
            pygame.display.flip()
            clock.tick(30)

    font = pygame.font.SysFont(None, 36)
    player_name = ask_player_name(screen, font)
    if player_name is None:
        return

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Shot.containers = (shots, updatable, drawable)

    # register explosion sprite containers so effects are added to groups
    from explosion import Explosion
    Explosion.containers = (updatable, drawable)

    # enable shot lifetime behavior
    import shot_patch

    # score counter
    score = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for sprite in drawable:
            sprite.draw(screen)

        # draw score and lives HUD
        score_surf = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))
        lives_surf = font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(lives_surf, (10, 40))

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                # remove the asteroid so it doesn't immediately re-hit the player
                asteroid.kill()
                player.lives -= 1
                if player.lives <= 0:
                    log_event("game_over")
                    print("Game over!")
                    print(f"Final score: {score}")
                    # save to leaderboard and show it
                    try:
                        from leaderboard import add_score, get_top

                        # check previous top to detect a new high score
                        top_before = get_top(10)
                        prev_top_score = top_before[0]['score'] if top_before else -1

                        add_score(player_name, score)
                        top = get_top(10)

                        # find player's entry index in the updated leaderboard
                        player_index = None
                        for i, e in enumerate(top):
                            if e.get('name') == player_name and e.get('score') == score:
                                player_index = i
                                break

                        # treat as new high only if player is at index 0 and score strictly greater than previous top
                        highlight_index = player_index if (player_index == 0 and score > prev_top_score) else None

                        def show_leaderboard(screen, font, top_entries, highlight_index=None):
                            clock = pygame.time.Clock()
                            start = time.time()
                            anim_duration = 2.0
                            anim_done = False
                            while True:
                                for event in pygame.event.get():
                                    # always allow window close
                                    if event.type == pygame.QUIT:
                                        return
                                    # only accept 'q' key after animation has finished
                                    if event.type == pygame.KEYDOWN and anim_done:
                                        if event.key == pygame.K_q:
                                            return

                                screen.fill("black")
                                title = font.render("Leaderboard", True, "white")
                                screen.blit(title, (50, 30))

                                for i, e in enumerate(top_entries, start=1):
                                    text = f"{i}. {e['name']} - {e['score']}"
                                    y = 30 + i * 30
                                    if highlight_index is not None and i - 1 == highlight_index:
                                        # pulsing highlight color
                                        t = time.time() - start
                                        color_val = 200 + int(55 * (0.5 + 0.5 * math.sin(t * 6)))
                                        color = (255, color_val, 0)
                                        rendered = font.render(text, True, color)
                                        screen.blit(rendered, (50, y))
                                    else:
                                        screen.blit(font.render(text, True, "white"), (50, y))

                                if highlight_index is not None and not anim_done:
                                    # 'New High Score!' pulsing text
                                    t = time.time() - start
                                    nh_color = (255, 50 + int(100 * (0.5 + 0.5 * math.sin(t * 6))), 50)
                                    nh_text = font.render("New High Score!", True, nh_color)
                                    rect = nh_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
                                    screen.blit(nh_text, rect)
                                else:
                                    # show a persistent hint to press Q to quit
                                    hint = font.render("Press Q to quit", True, "white")
                                    screen.blit(hint, (50, 400))

                                if not anim_done and time.time() - start >= anim_duration:
                                    anim_done = True

                                pygame.display.flip()
                                clock.tick(60)

                        show_leaderboard(screen, font, top, highlight_index)
                    except Exception:
                        pass
                    sys.exit()
                else:
                    log_event("player_respawn")
                    player.respawn()
                    break

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    # update score when an asteroid is shot
                    points = int(asteroid.radius) * 2
                    score += points
                    log_event("score_changed", score=score, points=points)
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000.0        

if __name__ == "__main__":
    main()