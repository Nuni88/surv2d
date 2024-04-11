import pygame
from weapon import Weapon
from constants import DISP_SCALE

vec = pygame.math.Vector2


class ProjWeapon(Weapon):
    def __init__(self, pos, ptype, delay_mod):
        super().__init__(pos, ptype, delay_mod)
        self.max_proj = 10

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)
