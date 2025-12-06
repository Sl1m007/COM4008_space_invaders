# main.py
"""
COM4008 – Programming Concepts
Coursework 1 – Space Invaders

This file is the main entry point for the game.
It creates the window, sets up the sprite groups, and runs the main game loop.
Other files provide the player, invader, bullet and barrier classes.
"""

import pygame
import sys
import random

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE,
    INVADER_SPEED_START, INVADER_DROP
)
from player import Player
from invader import create_invader_array
from barrier import create_barriers


# -------------------------------------------------------------------
# Helper function: find the lowest invader in each column
# Only these "bottom" invaders are allowed to shoot.
# This is similar to how classic Space Invaders behaves.
# -------------------------------------------------------------------
def get_bottom_invaders(invader_group):
    """Return a list of invaders that are the lowest in each column."""
    bottom_by_x = {}
    for inv in invader_group:
        x = inv.rect.x
        # For each x-position, keep the invader with the greatest y (lowest on screen)
        if x not in bottom_by_x or inv.rect.y > bottom_by_x[x].rect.y:
            bottom_by_x[x] = inv
    return list(bottom_by_x.values())


pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COM4008 Space Invaders - Terry (CW1)")

clock = pygame.time.Clock()
FPS = 60  # Target frames per second
font = pygame.font.Font(None, 36)

# -------------------------------------------------------------------
# Sprite groups
# These groups make it easier to update and draw related sprites together.
# -------------------------------------------------------------------
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
invader_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()          # Bullets fired by the player
barrier_group = pygame.sprite.Group()
invader_bullet_group = pygame.sprite.Group()  # Bullets fired by invaders

# -------------------------------------------------------------------
# Create the main game objects
# -------------------------------------------------------------------
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
player_group.add(player)
all_sprites.add(player)

# Create the grid of invaders and the protective barriers
create_invader_array(invader_group, all_sprites)
create_barriers(barrier_group, all_sprites)

# Basic game state variables
invader_speed = INVADER_SPEED_START
game_over = False
score = 0

# Invader shooting control:
# - invader_shot_cooldown stops them firing every frame
# - INVADER_SHOT_DELAY controls how often they can shoot
# - MAX_INVADER_BULLETS limits the number of enemy bullets on screen
invader_shot_cooldown = 0
INVADER_SHOT_DELAY = 30
MAX_INVADER_BULLETS = 5

# -------------------------------------------------------------------
# Main game loop
# This loop keeps running until the player closes the window.
# -------------------------------------------------------------------
running = True
while running:
    clock.tick(FPS)  # Keep the loop running at roughly 60 FPS

    # ------------- Event handling -------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Player has closed the window
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Player fires a bullet (if the game is still running)
                player.shoot(bullet_group, all_sprites)

    # Check which keys are currently held down
    keys = pygame.key.get_pressed()

    # ------------- Game logic -------------
    if not game_over:
        # Update player position based on keyboard input
        player.update(keys)

        # ---------------- Invader movement ----------------
        move_down = False

        # Move all invaders horizontally
        for inv in invader_group:
            inv.rect.x += invader_speed

        # Check if any invader has hit the left or right edge
        for inv in invader_group:
            if inv.rect.right >= SCREEN_WIDTH - 10 or inv.rect.left <= 10:
                move_down = True
                break

        # If an edge was hit, reverse direction and move the invaders down
        if move_down:
            invader_speed *= -1
            for inv in invader_group:
                inv.rect.y += INVADER_DROP

        # Increase invader speed as fewer of them remain
        if len(invader_group) > 0:
            increase = (30 - len(invader_group)) // 10
            invader_speed = (INVADER_SPEED_START + increase) * (1 if invader_speed > 0 else -1)

        # ---------------- Invader shooting ----------------
        # Reduce the cooldown timer if it is above zero
        if invader_shot_cooldown > 0:
            invader_shot_cooldown -= 1

        # Only attempt a shot if:
        # - the cooldown has finished, and
        # - there are not too many enemy bullets already on screen
        if invader_shot_cooldown == 0 and len(invader_bullet_group) < MAX_INVADER_BULLETS:
            bottom_invaders = get_bottom_invaders(invader_group)
            if bottom_invaders:
                # Pick one of the lowest invaders at random to be the shooter
                shooter = random.choice(bottom_invaders)
                # This random check controls how often they actually fire
                if random.randint(1, 90) == 1:
                    shooter.shoot(invader_bullet_group, all_sprites)
                    invader_shot_cooldown = INVADER_SHOT_DELAY

        # ---------------- Update bullets ----------------
        bullet_group.update()           # Player bullets
        invader_bullet_group.update()   # Enemy bullets

        # ---------------- Collisions ----------------
        # Player bullets hitting invaders
        hits = pygame.sprite.groupcollide(invader_group, bullet_group, True, True)
        score += len(hits)

        # Player bullets hitting barriers (remove both)
        pygame.sprite.groupcollide(barrier_group, bullet_group, True, True)

        # Invader bullets hitting barriers (also remove both)
        pygame.sprite.groupcollide(barrier_group, invader_bullet_group, True, True)

        # Invader bullets hitting the player
        player_hits = pygame.sprite.spritecollide(player, invader_bullet_group, True)
        if player_hits:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # Check if any invader has reached too close to the bottom of the screen
        for inv in invader_group:
            if inv.rect.bottom >= SCREEN_HEIGHT - 100:
                game_over = True

    # ------------- Drawing everything -------------
    screen.fill(BLACK)

    # Draw all sprites (player, invaders, bullets, barriers)
    all_sprites.draw(screen)

    # Draw the HUD (lives and score)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    # Show a simple GAME OVER message when the game has finished
    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    # Update the display with everything we have drawn
    pygame.display.flip()

# ------------- Clean exit -------------
pygame.quit()
sys.exit()