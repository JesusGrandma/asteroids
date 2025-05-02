import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroiodfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Astroids")
    clock = pygame.time.Clock()
    background = pygame.image.load("assets/space.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0
    score = 0
    lives = 3

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid) and player.invincible_timer <= 0:
                if lives > 0:
                    lives = lives - 1
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.start_invincibility(2.0)

                else:
                    print(f"Game Over! Final Score: {score}!")
                    pygame.quit()
                    sys.exit()
                break

        for asteroid in list(asteroids):  # safe to modify group
            for shot in list(shots):
                if shot.collides_with(asteroid):
                    asteroid.split()
                    shot.kill()
                    score += 100

        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        # Draw score AFTER everything else
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        text_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        text_rect2 = lives_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, text_rect)
        screen.blit(lives_text, text_rect2)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()