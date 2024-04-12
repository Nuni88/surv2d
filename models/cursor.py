import pygame
import os
from models.constants import DISP_SCALE

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
            else:
                self.rect.topleft = pygame.mouse.get_pos()

        except RuntimeError as e:
            raise

    def scale_to_screen(self, scale: float):
        try:
            if type(scale) is not float:
                raise TypeError
            else:
                self.image = pygame.transform.scale_by(self.image, scale)

        except TypeError as e:
            raise