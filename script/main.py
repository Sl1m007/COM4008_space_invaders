################################################################
# COM4008 – Programming Concepts
# Coursework 1 – Space Invaders
# Author: Terry Catchpole
################################################################

import pygame
import random
import sys
from pathlib import Path

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, INVADER_SPEED_START, INVADER_DROP
from player import Player
from invader import Invader
from invader_bullet import InvaderBullet
from barrier import create_barriers

pygame.init()

####################################### Screen Size ###################################
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("COM4008 Space Invaders - Terry (CW1)")

clock = pygame.time.Clock()
FPS = 60

############################### PATHS #######################################
BASE_DIR = Path(__file__).resolve().parent              # .../script
IMG_DIR = BASE_DIR.parent / "images" / "objects"        # .../images/objects

############################### CONSTANTS ##################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

PLAYER_SPEED = 5
BULLET_SPEED = -7

INVADER_SPEED_START = 1
INVADER_DROP = 20

font = pygame.font.Font(None, 36)


#======================================================================
#  BULLET CLASS
#======================================================================
class Bullet(pygame.sprite.Sprite):
    """A bullet fired by the player."""
    def __init__(self, x, y, speed_y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed_y = speed_y

    def update(self):
        """Move bullet up and delete if off-screen."""
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()








# ======================================================================
#  HELPER FUNCTIONS – CREATE INVADERS & BARRIERS
# ======================================================================

def create_invader_array(invaders, all_sprites, rows=3, cols=10, x_margin=100, y_margin=60, gap=10):
    """Create 3 rows of invaders using 3 sprite types."""
    images = ["invader1.png", "invader2.png", "invader3.png"]

    for row in range(rows):
        for col in range(cols):
            x = x_margin + col * (40 + gap)
            y = y_margin + row * (30 + gap)
            image = images[row % len(images)]
            inv = Invader(x, y, image)
            invaders.add(inv)
            all_sprites.add(inv)





# ======================================================================
#  GAME SETUP
# ======================================================================

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
invader_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
invader_bullet_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()

# Create player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
player_group.add(player)
all_sprites.add(player)

# Create invaders (Requirement 1)
create_invader_array(invader_group, all_sprites)

# Create barriers (Requirement 3)
create_barriers(barrier_group, all_sprites)

invader_speed = INVADER_SPEED_START
game_over = False
score = 0


# ======================================================================
#  GAME LOOP
# ======================================================================
running = True
while running:
    clock.tick(FPS)

# ---------------- EVENTS -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(bullet_group, all_sprites)   # Requirement 2

    keys = pygame.key.get_pressed()

# ---------------- GAME LOGIC -----------------
    if not game_over:

# Player movement
        player.update(keys)

# Move invaders horizontally
        move_down = False
        for inv in invader_group:
            inv.rect.x += invader_speed

# Check edges → drop down
        for inv in invader_group:
            if inv.rect.right >= SCREEN_WIDTH - 10 or inv.rect.left <= 10:
                move_down = True
                break

        if move_down:
            invader_speed *= -1  # Reverse direction
            for inv in invader_group:
                inv.rect.y += INVADER_DROP  # Drop down

# Speed up as invaders die
        if len(invader_group) > 0:
            increase = (30 - len(invader_group)) // 10
            invader_speed = (INVADER_SPEED_START + increase) * (1 if invader_speed > 0 else -1)

# Random invader shooting (sporadic)
        if random.randint(1, 30) == 1 and len(invader_group) > 0:
            shooter = random.choice(invader_group.sprites())
            bullet = InvaderBullet(shooter.rect.centerx, shooter.rect.bottom)
            invader_bullet_group.add(bullet)
            all_sprites.add(bullet)

# Update bullets
        bullet_group.update()
        invader_bullet_group.update()

# Player bullets hit invader
        hits = pygame.sprite.groupcollide(invader_group, bullet_group, True, True)
        score += len(hits)

# Player bullets hit barriers
        pygame.sprite.groupcollide(barrier_group, bullet_group, True, True)

# Invader bullets hit barriers
        pygame.sprite.groupcollide(barrier_group, invader_bullet_group, True, True)

# Invader bullets hit defender (lose life)
        if pygame.sprite.spritecollide(player, invader_bullet_group, True):
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

# GAME OVER if invaders reach too low
        for inv in invader_group:
            if inv.rect.bottom >= SCREEN_HEIGHT - 100:
                game_over = True

# ---------------- DRAWING -----------------
    screen.fill(BLACK)
    all_sprites.draw(screen)

# HUD
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

    pygame.display.flip()

# ---------------- DRAWING -----------------
screen.fill(BLACK)

all_sprites.draw(screen)

# HUD
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