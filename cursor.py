import pygame
import os

vec = pygame.math.Vector2


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images', 'menu_cursor.png'))
        self.rect = self.surf.get_rect()

    def move(self):
        self.rect.topleft = pygame.mouse.get_pos()