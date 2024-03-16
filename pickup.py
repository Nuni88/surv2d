import os
import pygame


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.surf = surf
        self.rect = self.surf.get_rect(center=pos)
        self.value = 0

    def scroll(self, offset):
        self.rect.centerx -= offset

    def get_value(self) -> int:
        return self.value


class ExpSmall(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_small.png')))
        self.value = 5


class ExpMed(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_med.png')))
        self.value = 20


class ExpLarge(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_large.png')))
        self.value = 50
