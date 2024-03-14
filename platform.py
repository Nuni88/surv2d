import os
import pygame

vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, c):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images\\environment', 'plat2.png'))
        self.rect = self.surf.get_rect(center=c)
        self.pos = vec(self.rect.midbottom)

    def move(self, pos):
        self.rect.centerx = pos

    def scroll(self, offset):
        self.pos.x -= offset
        self.rect.midbottom = self.pos