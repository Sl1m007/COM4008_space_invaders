# invader.py
"""
This file contains the Invader class and the function that creates the
grid of invaders shown at the top of the screen. Each invader has its
own sprite image and can fire bullets downwards at the player.
"""

import pygame
from settings import IMG_DIR
from invader_bullet import InvaderBullet


class Invader(pygame.sprite.Sprite):
    """
    Represents a single invader in the formation.
    Each invader is given an image and a starting position.
    """

    def __init__(self, x, y, img_name: str):
        super().__init__()

        # Load and scale the invader image
        img = pygame.image.load(str(IMG_DIR / img_name)).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 30))

        # Position the invader at the given coordinates
        self.rect = self.image.get_rect(topleft=(x, y))

    def shoot(self, invader_bullet_group, all_sprites):
        """
        Fire a bullet straight downwards from the centre of the invader.
        The new bullet is added to the relevant sprite groups so that it
        can be updated and drawn by the main game loop.
        """
        bullet = InvaderBullet(self.rect.centerx, self.rect.bottom)
        invader_bullet_group.add(bullet)
        all_sprites.add(bullet)


def create_invader_array(invaders, all_sprites,
                         rows=3, cols=10,
                         x_margin=100, y_margin=60, gap=10):
    """
    Create a grid of invaders arranged in rows and columns.

    Each row uses a different sprite to add variation. The spacing
    between invaders can be adjusted using the 'gap' parameter.
    """

    images = ["invader1.png", "invader2.png", "invader3.png"]

    for row in range(rows):
        for col in range(cols):
            # Calculate the x and y position for this invader
            x = x_margin + col * (40 + gap)
            y = y_margin + row * (30 + gap)

            # Pick the sprite for this row
            img_name = images[row % len(images)]

            # Create the invader and add it to the groups
            inv = Invader(x, y, img_name)
            invaders.add(inv)
            all_sprites.add(inv)