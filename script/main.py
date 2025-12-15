# filename: main.py
#
# COM4008 - Programming Concepts
# Coursework 1 - Space Invaders
#
# This is the main file that starts the game.
# It creates the window, sets everything up, and runs the main loop.
# All the other files handle different parts of the game like the player,
# invaders, bullets and barriers.

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


#########################################################################
# This function helps find the lowest invader in each column.
# Only the invaders at the bottom of their columns are allowed to shoot,
# which is similar to how shooting worked in classic Space Invaders.
#########################################################################

def get_bottom_invaders(invader_group):
    bottom_by_x = {}
    for inv in invader_group:
        x = inv.rect.x
        # For each x-value, keep whichever invader is lower on the screen.
        if x not in bottom_by_x or inv.rect.y > bottom_by_x[x].rect.y:
            bottom_by_x[x] = inv
    return list(bottom_by_x.values())

# Needed to initialise Pygame before creating the game window.
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COM4008 Space Invaders - Terry (CW1)")

clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 36)

###########################################################
# Sprite groups help keep all the game objects organised.
###########################################################
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
invader_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()          # Player bullets
barrier_group = pygame.sprite.Group()
invader_bullet_group = pygame.sprite.Group()  # Invader bullets

################################
# Create the main game objects
################################
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
player_group.add(player)
all_sprites.add(player)

create_invader_array(invader_group, all_sprites)
create_barriers(barrier_group, all_sprites)

# Game state
invader_speed = INVADER_SPEED_START
game_over = False
score = 0

# Invader shooting control
invader_shot_cooldown = 0
INVADER_SHOT_DELAY = 30
MAX_INVADER_BULLETS = 5

##################
# Main game loop
##################
running = True
while running:
    clock.tick(FPS)

    ########### Event handling #########
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(bullet_group, all_sprites)


    keys = pygame.key.get_pressed()

    ######### Game logic #########
    if not game_over:

        # Update player movement
        player.update(keys)

        # ----- Invader movement -----
        move_down = False

        # Move the invaders sideways
        for inv in invader_group:
            inv.rect.x += invader_speed

        # Check if any invader hit the edge
        for inv in invader_group:
            if inv.rect.right >= SCREEN_WIDTH - 10 or inv.rect.left <= 10:
                move_down = True
                break

        # Reverse direction and drop down
        if move_down:
            invader_speed *= -1
            for inv in invader_group:
                inv.rect.y += INVADER_DROP

        # Speed up as fewer invaders remain
        if len(invader_group) > 0:
            increase = (30 - len(invader_group)) // 10
            invader_speed = (INVADER_SPEED_START + increase) * (1 if invader_speed > 0 else -1)

        # ----- Invader shooting -----
        if invader_shot_cooldown > 0:
            invader_shot_cooldown -= 1

        if invader_shot_cooldown == 0 and len(invader_bullet_group) < MAX_INVADER_BULLETS:
            bottom_invaders = get_bottom_invaders(invader_group)
            if bottom_invaders:
                shooter = random.choice(bottom_invaders)
                # Small chance of actually firing
                if random.randint(1, 90) == 1:
                    shooter.shoot(invader_bullet_group, all_sprites)
                    invader_shot_cooldown = INVADER_SHOT_DELAY

        ######### Update bullets #######
        bullet_group.update()
        invader_bullet_group.update()

        ####### Collisions #######
        # Player bullets hit invaders
        hits = pygame.sprite.groupcollide(invader_group, bullet_group, True, True)
        score += len(hits)

        # Player bullets hit barriers
        pygame.sprite.groupcollide(barrier_group, bullet_group, True, True)

        # Invader bullets hit barriers
        pygame.sprite.groupcollide(barrier_group, invader_bullet_group, True, True)

        # Invader bullets hit player
        player_hits = pygame.sprite.spritecollide(player, invader_bullet_group, True)
        if player_hits:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # If invaders reach too low, game is over
        for inv in invader_group:
            if inv.rect.bottom >= SCREEN_HEIGHT - 100:
                game_over = True

    ########## Drawing everything #########
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # HUD (lives and score)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    pygame.display.flip()

########## Clean exit ###############
pygame.quit()
sys.exit()