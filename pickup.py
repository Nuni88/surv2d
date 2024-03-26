import os
import pygame
from constants import MAXHP, DISP_SCALE


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.surf = pygame.transform.scale_by(surf, DISP_SCALE)
        self.rect = self.surf.get_rect(center=pos)
        self.value = 0

    def scroll(self, offset):
        self.rect.centerx -= offset

    def get_value(self) -> int:
        return self.value

    def collect(self, player):
        pass

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)


class ExpPickup(Pickup):
    def __init__(self, pos, surf):
        super().__init__(pos, surf)
        self.value = 0

    '''
    def collect(self, player):
        player.gain_exp(self.value)
    '''


class ExpSmall(ExpPickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_small.png')))
        self.value = 5


class ExpMed(ExpPickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_med.png')))
        self.value = 20


class ExpLarge(ExpPickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'exp_large.png')))
        self.value = 50


class MaxHealthPickup(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'maxhp.png')))
        self.value = 10

    def collect(self, player):
        player.gain_stat_bonus(MAXHP, self.value)


class HealthPickup(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'potion_small.png')))
        self.value = 0.2

    def collect(self, player):
        player.heal_percent(self.value)
