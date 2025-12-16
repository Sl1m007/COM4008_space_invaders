import pygame
from settings import IMG_DIR, SCREEN_WIDTH, PLAYER_SPEED
from defender_bullet import DefenderBullet


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load(str(IMG_DIR / "defender.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (60, 35))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, bullet_group, all_sprites):
        bullet = DefenderBullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)
        all_sprites.add(bullet)