import os
import math
import pygame
from constants import FPS, STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2
# TODO: Read pickup attributes from file


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = pygame.transform.scale_by(image, DISP_SCALE)
        self.pos = vec(pos)
        self.rect = self.image.get_rect(center=pos)
        self.value = 0

    def update(self, ppos, range, offset):
        self.pos.x -= offset
        self.rect.center = self.pos

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
        self.vel = vec(0, 0)

    def update(self, ppos, range, offset):
        self.pos.x -= offset
        if self.pos.distance_to(ppos) <= range * DISP_SCALE:
            dx, dy = (ppos.x - self.pos.x, ppos.y - self.pos.y)
            self.vel = vec(dx / FPS, dy / FPS)
            self.pos += self.vel
        self.rect.center = self.pos


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
