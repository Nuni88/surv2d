from enum import Enum
import pygame
from projectile import Fireball, Iceball, Lightning
from constants import SHOOTING_DELAY

WEAPONTYPES = {
    'Fireball': Fireball,
    'Iceball': Iceball,
    'Lightning': Lightning
}


class Emitter(pygame.sprite.Sprite):
    def __init__(self, proj_type, pos, acc):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(center=pos)
        self.bullets = []
        self.shot_timer = 0
        self.delay = SHOOTING_DELAY
        self.acc = acc
        self.proj_type = WEAPONTYPES[proj_type]

    def move(self, loc):
        self.rect.center = loc
        for bullet in self.bullets:
            if bullet.move():
                self.bullets.remove(bullet)

    def shoot(self):
        bullet = self.proj_type(self.rect.center, self.acc)
        self.bullets.append(bullet)
        print(f'Fire! Bullets fired: {len(self.bullets)}')

    def get_bullets(self) -> list:
        return self.bullets

    def update(self, ms):
        for bullet in self.bullets:
            bullet.update(ms)
        self.shot_timer += ms
        if self.shot_timer >= self.delay:
            self.shoot()
            self.shot_timer -= self.delay
