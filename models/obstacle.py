import os
import pygame
from models.constants import DISP_SCALE

vec = pygame.math.Vector2


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, c: pygame.math.Vector2, image: str):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join('images/environment', image)), DISP_SCALE)
        self.rect = self.image.get_rect(center=c)
        self.pos = vec(self.rect.midbottom)

    def update(self, offset: float):
        self.pos.x -= offset
        self.rect.midbottom = self.pos

    def scale_to_screen(self, scale: float):
        self.image = pygame.transform.scale_by(self.image, scale)

    def recenter(self, pos: pygame.math.Vector2):
        self.pos.x = pos.x
        self.rect.midbottom = self.pos
