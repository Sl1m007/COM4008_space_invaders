################################################################
# COM4008 – Programming Concepts
# Coursework 1 – Space Invaders (All 3 Requirements Completed)
#
# This main.py script implements:
# 1. Invader Array (3 sprite types, movement left/right, dropping down, speeding up)
# 2. Player Shooting (multiple bullets, collisions, lives)
# 3. Barriers (crumble when hit)
#
# Folder Structure:
# space_invaders/
#  images/
#    objects/
#      defender.png
#      invader1.png
#      invader2.png
#      invader3.png
#  script/
#    main.py
#
# Author: Terry Catchpole
########################################################################################

import pygame
import random
import sys
from pathlib import Path
from defender_bullet import DefenderBullet


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


# ======================================================================
#  PLAYER CLASS
# ======================================================================
class Player(pygame.sprite.Sprite):
    # The defender that moves left/right and shoots bullets.
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load(str(IMG_DIR / "defender.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (60, 35))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.lives = 3

    def update(self, keys):
        """Move left/right while staying on screen."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Stop leaving screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, bullet_group, all_sprites):
        # Create a bullet above the player."""
        bullet = DefenderBullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)
        all_sprites.add(bullet)

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


#======================================================================
#  INVADER CLASS
#======================================================================
class Invader(pygame.sprite.Sprite):
    """Single invader inside the array."""
    def __init__(self, x, y, img_path):
        super().__init__()
        img = pygame.image.load(str(IMG_DIR / img_path)).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 30))
        self.rect = self.image.get_rect(topleft=(x, y))


# ======================================================================
#  BARRIER BLOCK CLASS
# ======================================================================
class BarrierBlock(pygame.sprite.Sprite):
    """Small piece of barrier that disappears when hit."""
    def __init__(self, x, y, size=6):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


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


def create_barrier(barrier_group, all_sprites, start_x, start_y):
    """Make a grid of little blocks to form a barrier."""
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
    """Place 4 barriers across the screen."""
    base_y = SCREEN_HEIGHT - 150
    spacing = 150

    for i in range(4):
        start_x = 120 + i * spacing
        create_barrier(barrier_group, all_sprites, start_x, base_y)


# ======================================================================
#  GAME SETUP
# ======================================================================

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
invader_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
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

# End the game if invaders reach the defensive barriers
# This prevents invaders passing through the player's last line of defence

        if pygame.sprite.groupcollide(invader_group, barrier_group, False, False):
            game_over = True

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

        # Update bullets
        bullet_group.update()

        # Bullet hits invader (Req 2)
        hits = pygame.sprite.groupcollide(invader_group, bullet_group, True, True)
        score += len(hits)

        # Bullet hits barrier (Req 3 – crumbling)
        pygame.sprite.groupcollide(barrier_group, bullet_group, True, True)

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

pygame.quit()
sys.exit()