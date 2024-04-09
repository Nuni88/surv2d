from weapon import Weapon, WEAPONDATA
from constants import STAT_STRS, DISP_SCALE

WEAPONS = WEAPONDATA['Melee']


class MeleeWeapon(Weapon):
    def __init__(self, pos, data):
        super().__init__(pos, data)
        self.max_proj = 1

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)


class FireWheel(MeleeWeapon):
    def __init__(self, pos):
        super().__init__(pos, WEAPONS['Fire'])


class KatanaW(MeleeWeapon):
    def __init__(self, pos):
        super().__init__(pos, WEAPONS['Kat'])
