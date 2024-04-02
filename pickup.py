import os
import pygame
from constants import STAT_STRS, DISP_SCALE


# TODO: Read pickup attributes from file


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = pygame.transform.scale_by(image, DISP_SCALE)
        self.rect = self.image.get_rect(center=pos)
        self.value = 0

    def update(self, offset):
        self.rect.centerx -= offset

    def get_value(self) -> int:
        return self.value

    def collect(self, player):
        pass

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)


class ExpPickup(Pickup):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.value = 0


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
        player.gain_stat_bonus(STAT_STRS['MAXHP'], self.value)


class HealthPickup(Pickup):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(os.path.join('images\\pickups', 'potion_small.png')))
        self.value = 0.2

    def collect(self, player):
        player.heal_percent(self.value)
