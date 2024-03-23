import os
import pygame

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
    def __init__(self, c, surf):
        super().__init__(c, surf)
        self.lock_surf = None
        self.lock_lvl_surf = None
        self.lock = {
            'typ': 'Weapon',
            'req': 'FireShooter',
            'req_lvl': 5
        }

    def display_lock(self):
        pass

    def can_unlock(self, player) -> bool:
        return False
