import pygame
from models.weapon import Weapon
from models.projectile import Projectile, Fireball, Katana
from globals.constants import DISP_SCALE

vec = pygame.math.Vector2


class MeleeWeapon(Weapon):
    def __init__(self, pos: pygame.math.Vector2, ptype: Projectile, delay_mod: float):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 1

    def update(self, loc: pygame.math.Vector2, offset: float, time_update: int, mods: dict, dist: pygame.math.Vector2):
        super().update(loc, offset, time_update, mods, dist)


class FireWheel(MeleeWeapon):
    def __init__(self, pos: pygame.math.Vector2):
        super().__init__(pos, Fireball, 1.0)
        self.nodes.append(vec(-35.0, 0.0) * DISP_SCALE)
        self.nodes.append(vec(-70.0, 0.0) * DISP_SCALE)


class KatanaW(MeleeWeapon):
    def __init__(self, pos: pygame.math.Vector2):
        super().__init__(pos, Katana, 1.5)
        self.nodes.append(vec(-18.0, -15.0) * DISP_SCALE)
        self.nodes.append(vec(18.0, -15.0) * DISP_SCALE)
