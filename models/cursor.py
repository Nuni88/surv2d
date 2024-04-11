import pygame
import os
from models.constants import DISP_SCALE

vec = pygame.math.Vector2
IMG_PATH = '../images'


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join(IMG_PATH, 'menu_cursor.png')), DISP_SCALE)
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)
