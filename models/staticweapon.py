import pygame
from weapon import Weapon
from projectile import Projectile, Iceball
from constants import DISP_SCALE

vec = pygame.math.Vector2


class StaticWeapon(Weapon):
    def __init__(self, pos: pygame.math.Vector2, ptype: Projectile, delay_mod: float):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 5

    def update(self, loc: pygame.math.Vector2, offset: float, time_update: int, mods: dict, dist: pygame.math.Vector2):
        super().update(loc, offset, time_update, mods, dist)


class IceMine(StaticWeapon):
    def __init__(self, pos: pygame.math.Vector2):
        super().__init__(pos, Iceball, 1.5)
        self.nodes.append(vec(-30.0, 20.0) * DISP_SCALE)
        self.nodes.append(vec(30.0, 20.0) * DISP_SCALE)
