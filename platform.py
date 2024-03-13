import os
import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, c):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images\\environment', 'plat1.png'))
        self.rect = self.surf.get_rect(center=c)
