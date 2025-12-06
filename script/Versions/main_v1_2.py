# main.py
"""
COM4008 – Programming Concepts
Coursework 1 – Space Invaders

This script glues together:
- Player (player.py)
- Bullet (bullet.py)
- Invaders (invader.py)
- Barriers (barrier.py)
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

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COM4008 Space Invaders - Terry (CW1)")

clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 36)

# Sprite groups
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
invader_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()          # player bullets
barrier_group = pygame.sprite.Group()
invader_bullet_group = pygame.sprite.Group()  # NEW: invader bullets

# Create objects
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
player_group.add(player)
all_sprites.add(player)

create_invader_array(invader_group, all_sprites)
create_barriers(barrier_group, all_sprites)

invader_speed = INVADER_SPEED_START
game_over = False
score = 0

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(bullet_group, all_sprites)

    keys = pygame.key.get_pressed()

    # Logic
    if not game_over:
        player.update(keys)

        # Move invaders left/right
        move_down = False
        for inv in invader_group:
            inv.rect.x += invader_speed

        for inv in invader_group:
            if inv.rect.right >= SCREEN_WIDTH - 10 or inv.rect.left <= 10:
                move_down = True
                break

        if move_down:
            invader_speed *= -1
            for inv in invader_group:
                inv.rect.y += INVADER_DROP

        # Speed up as fewer invaders remain
        if len(invader_group) > 0:
            increase = (30 - len(invader_group)) // 10
            invader_speed = (INVADER_SPEED_START + increase) * (1 if invader_speed > 0 else -1)

        # --- RANDOM INVADER SHOOTING (FIXED INDENTATION) ---
        for inv in invader_group:
            if random.randint(1, 250) == 1:  # lower number = more bullets
                inv.shoot(invader_bullet_group, all_sprites)

        # Update bullets
        bullet_group.update()           # player bullets
        invader_bullet_group.update()   # NEW: invader bullets

        # --- Collisions: player bullets vs invaders ---
        hits = pygame.sprite.groupcollide(invader_group, bullet_group, True, True)
        score += len(hits)

        # Player bullets vs barriers (crumbling)
        pygame.sprite.groupcollide(barrier_group, bullet_group, True, True)

        # Invader bullets vs barriers
        pygame.sprite.groupcollide(barrier_group, invader_bullet_group, True, True)

        # Invader bullets vs player
        player_hits = pygame.sprite.spritecollide(player, invader_bullet_group, True)
        if player_hits:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # GAME OVER if invaders reach too low
        for inv in invader_group:
            if inv.rect.bottom >= SCREEN_HEIGHT - 100:
                game_over = True

    # Drawing
    screen.fill(BLACK)

    # all_sprites already contains bullets, but we also keep
    # invader_bullet_group here for clarity if you want to debug.
    all_sprites.draw(screen)
    # invader_bullet_group.draw(screen)  # optional, as they're in all_sprites already

    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()