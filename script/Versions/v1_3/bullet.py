# file name: bullet.py
"""
This file defines the Bullet class used for the player's shots.
A bullet travels straight upwards until it either hits something
or goes off the top of the screen.
"""

import pygame
from settings import WHITE, BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    """
    A bullet fired by the player. It is represented by a small white
    rectangle and moves upwards each frame.
    """

    def __init__(self, x, y):
        super().__init__()

        # Create a simple rectangular shape for the bullet
        self.image = pygame.Surface((4, 12))
        self.image.fill(WHITE)

        # Position the bullet so it starts at the top-middle of the player
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Bullet speed is negative because it travels upwards
        self.speed_y = BULLET_SPEED

    def update(self):
        """
        Move the bullet upwards. If it leaves the screen, remove it to keep
        the game efficient and avoid unnecessary sprites.
        """
        self.rect.y += self.speed_y

        # Remove the bullet once it moves off the screen
        if self.rect.bottom < 0:
            self.kill()