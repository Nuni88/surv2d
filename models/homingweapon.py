import pygame
from weapon import Weapon
from projectile import Projectile, Lightning
from constants import DISP_SCALE

vec = pygame.math.Vector2


class HomingWeapon(Weapon):
    def __init__(self, pos: pygame.math.Vector2, ptype: Projectile, delay_mod: float):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 3

    def update(self, loc: pygame.math.Vector2, offset: float, time_update: int, mods: dict, dist: pygame.math.Vector2):
        super().update(loc, offset, time_update, mods, dist)


class LitStrike(HomingWeapon):
    def __init__(self, pos: pygame.math.Vector2):
        super().__init__(pos, Lightning, 0.8)
        self.nodes.append(vec(0.0, 0.0) * DISP_SCALE)
        self.nodes.append(vec(0.0, -30.0) * DISP_SCALE)
        self.nodes.append(vec(0.0, 30.0) * DISP_SCALE)
