import pygame
from weapon import Weapon
from projectile import Iceball
from constants import DISP_SCALE

vec = pygame.math.Vector2


class StaticWeapon(Weapon):
    def __init__(self, pos, ptype, delay_mod):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 5

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)


class IceMine(StaticWeapon):
    def __init__(self, pos):
        super().__init__(pos, Iceball, 1.5)
        self.nodes.append(vec(-30.0, 20.0) * DISP_SCALE)
        self.nodes.append(vec(30.0, 20.0) * DISP_SCALE)
