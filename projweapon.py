from weapon import Weapon, WEAPONDATA
from constants import STAT_STRS, DISP_SCALE

WEAPONS = WEAPONDATA['Proj']


class ProjWeapon(Weapon):
    def __init__(self, pos, data):
        super().__init__(pos, data)

    def update(self, loc, offset, time_update, mods, dist):
        super().update(loc, offset, time_update, mods, dist)
