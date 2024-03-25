import os
import pygame
from constants import LOCK_IMG_PATHS, LOCK_NUM_PATHS

vec = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, c, surf):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images\\environment', surf))
        self.rect = self.surf.get_rect(center=c)
        self.pos = vec(self.rect.midbottom)

    def scroll(self, offset):
        self.pos.x -= offset
        self.rect.midbottom = self.pos

    def recenter(self, player):
        self.pos.x = player.rect.centerx
        self.rect.midbottom = self.pos


class Door(Platform):
    def __init__(self, c, surf, req, lvl):
        super().__init__(c, surf)
        self.lock_base_surf = pygame.image.load(LOCK_IMG_PATHS['Base'])
        self.lock_req_surf = pygame.image.load(LOCK_IMG_PATHS[req])
        self.lock_lvl_surf = pygame.image.load(LOCK_NUM_PATHS[lvl])
        self.lock = {
            'req': req,
            'lvl': lvl
        }

    def display_lock(self):
        self.surf.blit(self.lock_base_surf, (1, self.rect.height * 0.3))
        self.surf.blit(self.lock_req_surf, (2, self.rect.height * 0.3 + 1))
        self.surf.blit(self.lock_base_surf, (1, self.rect.height * 0.6))
        self.surf.blit(self.lock_lvl_surf, (5, self.rect.height * 0.6 + 1))

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
