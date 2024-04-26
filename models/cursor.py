import pygame
import os
from globals.constants import DISP_SCALE

vec = pygame.math.Vector2


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join('images', 'menu_cursor.png')), DISP_SCALE)
        self.rect = self.image.get_rect()

    def move(self):
        try:
            if not pygame.get_init():
                raise RuntimeError

        except RuntimeError as e:
            raise

        else:
            self.rect.topleft = pygame.mouse.get_pos()

    def scale_to_screen(self, scale: float):
        try:
            if type(scale) is not float:
                raise TypeError

        except TypeError as e:
            raise

        else:
            self.image = pygame.transform.scale_by(self.image, scale)
