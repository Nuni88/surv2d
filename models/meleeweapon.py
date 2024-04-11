import pygame
from weapon import Weapon
from projectile import Fireball, Katana
from constants import DISP_SCALE

vec = pygame.math.Vector2


class MeleeWeapon(Weapon):
    def __init__(self, pos, ptype, delay_mod):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 1

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)


class FireWheel(MeleeWeapon):
    def __init__(self, pos):
        super().__init__(pos, Fireball, 1.0)
        self.nodes.append(vec(-35.0, 0.0) * DISP_SCALE)
        self.nodes.append(vec(-70.0, 0.0) * DISP_SCALE)


class KatanaW(MeleeWeapon):
    def __init__(self, pos):
        super().__init__(pos, Katana, 1.5)
        self.nodes.append(vec(-20.0, -20.0) * DISP_SCALE)
        self.nodes.append(vec(20.0, -20.0) * DISP_SCALE)
