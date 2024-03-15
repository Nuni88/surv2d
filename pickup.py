import os
import pygame


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.surf = surf
        self.rect = self.surf.get_rect(center=pos)

    def scroll(self, offset):
        self.rect.centerx -= offset


class ExpPickup(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_small.png')))
