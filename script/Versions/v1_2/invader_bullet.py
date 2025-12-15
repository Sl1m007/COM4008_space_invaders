# file name: invader_bullet.py
#########################################################################
# This file contains the InvaderBullet class, which represents the bullets
# fired by the invaders. These bullets travel downwards and disappear once
# they move off the bottom of the screen.
##########################################################################

import pygame
from settings import WHITE


class InvaderBullet(pygame.sprite.Sprite):
    ######################################################################
    # A bullet fired by an invader. It is drawn as a small white rectangle
    # and moves down the screen until it either hits something or leaves
    # the visible play area.
    ######################################################################

    def __init__(self, x, y):
        super().__init__()

        # Create a simple rectangular shape for the bullet
        self.image = pygame.Surface((4, 12))
        self.image.fill(WHITE)

        # Start the bullet just beneath the invader that fired it
        self.rect = self.image.get_rect(midtop=(x, y))

        # Positive value because the bullet travels downwards
        self.speed_y = 2

    def update(self):
        #################################################################
        # Move the bullet down the screen. If the bullet goes below the
        # bottom edge, remove it to avoid unnecessary processing.
        #################################################################
        self.rect.y += self.speed_y

        # Remove the bullet once it leaves the screen
        if self.rect.top > 600:
            self.kill()