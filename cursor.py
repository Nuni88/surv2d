import pygame
import os
from constants import DISP_SCALE

vec = pygame.math.Vector2


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale_by(pygame.image.load(os.path.join('images', 'menu_cursor.png')), DISP_SCALE)
        self.rect = self.surf.get_rect()

    def move(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)
