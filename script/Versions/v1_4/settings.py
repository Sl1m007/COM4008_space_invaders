# settings.py
from pathlib import Path

# ---- ABSOLUTE PATH TO YOUR IMAGES ----
IMG_DIR = Path(
    r"C:\Users\Admin\OneDrive - Buckinghamshire New University\COM4008_Program_CW1\space_invaders\images\objects"
)

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Speeds and behaviour
PLAYER_SPEED = 5
BULLET_SPEED = -7
INVADER_SPEED_START = 1
INVADER_DROP = 20