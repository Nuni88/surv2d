import os
import pygame
from platform import Platform
from constants import STAT_STRS, DISP_SCALE


# Modifiable values
# Paths to lock icons for locked doors
LOCK_PATH = 'images\\environment\\locks'
LOCK_IMG_PATHS = {
    'Base': os.path.join(LOCK_PATH, 'lock_base.png'),
    'FireShooter': os.path.join(LOCK_PATH, 'fire.png'),
    'LitShooter': os.path.join(LOCK_PATH, 'lit.png'),
    'IceShooter': os.path.join(LOCK_PATH, 'ice.png'),
    STAT_STRS['MAXHP']: os.path.join(LOCK_PATH, 'maxhp.png'),
    STAT_STRS['CRITC']: os.path.join(LOCK_PATH, 'critc.png'),
    STAT_STRS['ASPD']: os.path.join(LOCK_PATH, 'aspd.png'),
    STAT_STRS['MSPD']: os.path.join(LOCK_PATH, 'mspd.png'),
    STAT_STRS['JUMPH']: os.path.join(LOCK_PATH, 'jumph.png'),
    STAT_STRS['DODGE']: os.path.join(LOCK_PATH, 'dodge.png'),
    STAT_STRS['INVUL']: os.path.join(LOCK_PATH, 'invul.png'),
    STAT_STRS['DMG']: os.path.join(LOCK_PATH, 'dmg.png'),
    STAT_STRS['CRITD']: os.path.join(LOCK_PATH, 'critd.png'),
    STAT_STRS['PROJSPD']: os.path.join(LOCK_PATH, 'projspd.png'),
    STAT_STRS['PROJSZ']: os.path.join(LOCK_PATH, 'projsz.png'),
    STAT_STRS['PROJNUM']: os.path.join(LOCK_PATH, 'projnum.png')
}
LOCK_NUM_PATHS = {
    0: os.path.join(LOCK_PATH, 'lock_0.png'),
    1: os.path.join(LOCK_PATH, 'lock_1.png'),
    2: os.path.join(LOCK_PATH, 'lock_2.png'),
    3: os.path.join(LOCK_PATH, 'lock_3.png'),
    4: os.path.join(LOCK_PATH, 'lock_4.png'),
    5: os.path.join(LOCK_PATH, 'lock_5.png'),
    6: os.path.join(LOCK_PATH, 'lock_6.png'),
    7: os.path.join(LOCK_PATH, 'lock_7.png'),
    8: os.path.join(LOCK_PATH, 'lock_8.png'),
    9: os.path.join(LOCK_PATH, 'lock_9.png')
}
LOCK_DIST = 0.32


class Door(Platform):
    def __init__(self, c, surf, req, lvl):
        super().__init__(c, surf)
        self.lock_base_surf = pygame.transform.scale_by(pygame.image.load(LOCK_IMG_PATHS['Base']), DISP_SCALE)
        self.lock_req_surf = pygame.transform.scale_by(pygame.image.load(LOCK_IMG_PATHS[req]), DISP_SCALE)
        self.lock_lvl_surf = pygame.transform.scale_by(pygame.image.load(LOCK_NUM_PATHS[lvl]), DISP_SCALE)
        self.lock = {
            'req': req,
            'lvl': lvl
        }

    def display_lock(self):
        base_width = self.lock_base_surf.get_width()
        base_height = self.lock_base_surf.get_height()
        req_width = self.lock_req_surf.get_width()
        req_height = self.lock_req_surf.get_height()
        lvl_width = self.lock_lvl_surf.get_width()
        lvl_height = self.lock_lvl_surf.get_height()

        # Display locks centered on door with equal space above top lock and below bottom lock
        # Space above and below is LOCK_DIST * door height
        h = self.rect.height * LOCK_DIST
        # self.surf.blit(self.lock_base_surf, (self.rect.width * 0.5 - base_width * 0.5, h))
        # h = h + base_height * 0.5 - req_height * 0.5
        self.surf.blit(self.lock_req_surf, (self.rect.width * 0.5 - req_width * 0.5, h))
        h = self.rect.height - self.rect.height * LOCK_DIST - base_height
        self.surf.blit(self.lock_base_surf, (self.rect.width * 0.5 - base_width * 0.5, h))
        h = h + base_height * 0.5 - lvl_height * 0.5
        self.surf.blit(self.lock_lvl_surf, (self.rect.width * 0.5 - lvl_width * 0.5, h))

    def unlockable(self, player) -> bool:
        return False


class WeapDoor(Door):
    def __init__(self, c, surf, req, lvl):
        super().__init__(c, surf, req, lvl)

    def unlockable(self, player) -> bool:
        return player.has_req_weapon(self.lock['req'], self.lock['lvl'])


class StatDoor(Door):
    def __init__(self, c, surf, req, lvl):
        super().__init__(c, surf, req, lvl)

    def unlockable(self, player) -> bool:
        return player.has_req_stat(self.lock['req'], self.lock['lvl'])
