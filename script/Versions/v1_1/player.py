# player.py
##########################################################################
# This file contains the Player class, which represents the defender at the
# bottom of the screen. The player can move left and right and fire bullets
# upwards. The player also keeps track of their remaining lives.
##########################################################################

import pygame
from settings import IMG_DIR, SCREEN_WIDTH, PLAYER_SPEED
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    ########################################################################
    # The Player sprite represents the defender controlled by the user.
    # It loads the defender image, handles movement, and can shoot bullets.
    ########################################################################

    def __init__(self, x, y):
        super().__init__()

        # Load and scale the defender image
        img = pygame.image.load(str(IMG_DIR / "defender.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (60, 35))

        # Position the player so that the bottom of the sprite sits at (x, y)
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Number of lives the player starts with
        self.lives = 3

    def update(self, keys):
        #####################################################################
        # Move the player left or right depending on which arrow keys are held.
        # The player cannot move off the screen.
        #####################################################################
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Make sure the player stays within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, bullet_group, all_sprites):
        #####################################################################
        # Fire a bullet upwards from the centre of the player.
        # The new bullet is added to the relevant sprite groups so it can be
        # drawn and updated by the main game loop.
        #####################################################################
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)
        all_sprites.add(bullet)