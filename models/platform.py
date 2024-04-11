import os
import pygame
from constants import DISP_SCALE

vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, c, image):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join('../images/environment', image)), DISP_SCALE)
        self.rect = self.image.get_rect(center=c)
        self.pos = vec(self.rect.midbottom)

    def update(self, offset):
        self.pos.x -= offset
        self.rect.midbottom = self.pos

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)

    def recenter(self, pos):
        self.pos.x = pos.x
        self.rect.midbottom = self.pos
