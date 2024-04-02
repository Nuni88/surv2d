import os
import pygame
from constants import DISP_SCALE

vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, c, surf):
        super().__init__()
        self.surf = pygame.transform.scale_by(pygame.image.load(os.path.join('images\\environment', surf)), DISP_SCALE)
        self.rect = self.surf.get_rect(center=c)
        self.pos = vec(self.rect.midbottom)

    def update(self, offset):
        self.pos.x -= offset
        self.rect.midbottom = self.pos

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)

    def recenter(self, pos):
        self.pos.x = pos.x
        self.rect.midbottom = self.pos
