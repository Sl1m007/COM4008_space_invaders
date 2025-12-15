# barrier.py
# file name: barrier.py
#############################################################################
# This file contains the code for the barriers that protect the player.
# Each barrier is made up of many small blocks. When a bullet hits a block,
# only that piece is removed, which makes the barriers slowly crumble as
# the game continues.
#############################################################################

import pygame
from settings import GREEN, SCREEN_HEIGHT

class BarrierBlock(pygame.sprite.Sprite):
    #  Small piece of barrier that disappears when hit.
    def __init__(self, x, y, size=6):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


def create_barrier(barrier_group, all_sprites, start_x, start_y):
    # Make a grid of little blocks to form a barrier.
    width = 10      # 10 blocks wide
    height = 5      # 5 blocks tall

    for row in range(height):
        for col in range(width):
            x = start_x + col * 6
            y = start_y + row * 6
            block = BarrierBlock(x, y)
            barrier_group.add(block)
            all_sprites.add(block)


def create_barriers(barrier_group, all_sprites):
    # Place 4 barriers across the screen.
    base_y = SCREEN_HEIGHT - 150
    spacing = 150

    for i in range(4):
        start_x = 120 + i * spacing
        create_barrier(barrier_group, all_sprites, start_x, base_y)