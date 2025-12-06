# barrier.py
"""
This file contains the code for the barriers that protect the player.
Each barrier is made up of many small blocks. When a bullet hits a block,
only that piece is removed, which makes the barriers slowly crumble as
the game continues.
"""

import pygame
from settings import GREEN, SCREEN_HEIGHT


class BarrierBlock(pygame.sprite.Sprite):
    """
    A single small square block used to build the barriers.
    When a block is hit by any bullet, it is removed from the game.
    """

    def __init__(self, x, y, size=6):
        super().__init__()

        # Draw a tiny green square to represent a piece of the barrier
        self.image = pygame.Surface((size, size))
        self.image.fill(GREEN)

        # Position the block on screen
        self.rect = self.image.get_rect(topleft=(x, y))


# ---------------------------------------------------------------------
# A simple arch-shaped barrier made from ASCII characters.
# A "#" means "place a block here", and a space means empty air.
# This gives the barriers a more classic Space Invaders look.
# ---------------------------------------------------------------------
ARCH_SHAPE = [
    "    ####    ",
    "  ########  ",
    " ###    ### ",
    "###     ####",
    "###     ####",
]


def create_barrier(barrier_group, all_sprites, start_x, start_y, block_size=6):
    """
    Build a single barrier using the ARCH_SHAPE pattern above.
    Each "#" is replaced with a BarrierBlock at the correct position.
    """
    for row_index, row in enumerate(ARCH_SHAPE):
        for col_index, char in enumerate(row):
            if char == "#":
                x = start_x + col_index * block_size
                y = start_y + row_index * block_size

                block = BarrierBlock(x, y, block_size)
                barrier_group.add(block)
                all_sprites.add(block)


def create_barriers(barrier_group, all_sprites):
    """
    Place several barriers across the lower part of the screen.
    The spacing can be adjusted to spread them out evenly.
    """

    base_y = SCREEN_HEIGHT - 150   # Height where all barriers sit
    spacing = 160                  # Distance between each barrier

    # Create 4 barriers evenly spaced across the screen
    for i in range(4):
        start_x = 100 + i * spacing
        create_barrier(barrier_group, all_sprites, start_x, base_y)