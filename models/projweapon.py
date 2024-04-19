import pygame
from models.weapon import Weapon
from models.projectile import Projectile
from globals.constants import DISP_SCALE

vec = pygame.math.Vector2


class ProjWeapon(Weapon):
    def __init__(self, pos: pygame.math.Vector2, ptype: Projectile, delay_mod: float):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 10

    def update(self, loc: pygame.math.Vector2, offset: float, time_update: int, mods: dict, dist: pygame.math.Vector2):
        super().update(loc, offset, time_update, mods, dist)
