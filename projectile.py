import os
import math
import pygame
from constants import WIDTH, HEIGHT

vec = pygame.math.Vector2


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, acc, surf):
        super().__init__()
        self.surf = surf
        self.rect = self.surf.get_rect(center=pos)
        self.vel = vec(0, 0)
        self.acc = acc
        self.timer = 0

    def move(self) -> bool:
        self.vel += self.acc
        self.rect.center += self.vel

        if self.rect.left > WIDTH or self.rect.right < 0:
            return True
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            return True

        return False

    def update(self, ms):
        self.timer += ms


class Fireball(Projectile):
    def __init__(self, pos, acc):
        super().__init__(pos, acc, pygame.image.load(os.path.join('images\\projectiles', 'fire.png')))


class Iceball(Projectile):
    def __init__(self, pos, acc):
        super().__init__(pos, acc, pygame.image.load(os.path.join('images\\projectiles', 'ice.png')))


class Lightning(Projectile):
    def __init__(self, pos, acc):
        super().__init__(pos, acc, pygame.image.load(os.path.join('images\\projectiles', 'lit.png')))
