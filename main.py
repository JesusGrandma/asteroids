import pygame
import sys
from constants import *


def main():
    pygame.init
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Game")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        pygame.display.flip()

    print(f"Starting Asteroids! Screen width: {SCREEN_WIDTH} Screen height: {SCREEN_HEIGHT}")



if __name__ == "__main__":
    main()