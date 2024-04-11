import pygame
from weapon import Weapon
from projectile import Lightning
from constants import DISP_SCALE

vec = pygame.math.Vector2


class HomingWeapon(Weapon):
    def __init__(self, pos, ptype, delay_mod):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 3

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)


class LitStrike(HomingWeapon):
    def __init__(self, pos):
        super().__init__(pos, Lightning, 0.8)
        self.nodes.append(vec(0.0, 0.0) * DISP_SCALE)
        self.nodes.append(vec(0.0, -30.0) * DISP_SCALE)
        self.nodes.append(vec(0.0, 30.0) * DISP_SCALE)
