import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroiodfield import AsteroidField
from shot import Shot

background = pygame.image.load("assets/space.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_start_screen(screen, font, background):
    screen.blit(background, (0, 0))

    title_text = font.render("Asteroids", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

def draw_game_over_screen(screen, font, background, score):
    screen.blit(background, (0, 0))

    game_over_text = font.render("YOU LOSE", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press ENTER to Replay", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = 3

    draw_start_screen(screen, font, background)

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)

    while True:
        # Setup containers
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Player.containers = updatable, drawable
        Asteroid.containers = asteroids, updatable, drawable
        AsteroidField.containers = updatable
        Shot.containers = shots, updatable, drawable

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()

        lives = 3
        score = 0

        # Gameplay loop
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            updatable.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid) and player.invincible_timer <= 0:
                    lives -= 1
                    player.start_invincibility(2.0)
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

                    if lives <= 0:
                        draw_game_over_screen(screen, font, background, score)

                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        waiting = False
                                        playing = False
                                    elif event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()

            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        asteroid.split()
                        shot.kill()
                        score += 100

            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for obj in drawable:
                obj.draw(screen)

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(score_text, score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10)))
            screen.blit(lives_text, lives_text.get_rect(topleft=(10, 10)))

            pygame.display.flip()
            dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
