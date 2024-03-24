from enum import Enum
import pygame
from projectile import Fireball, Iceball, Lightning
from constants import SHOOTING_DELAY

vec = pygame.math.Vector2
'''
WEAPONTYPES = {
    'Fireball': Fireball,
    'Iceball': Iceball,
    'Lightning': Lightning
}
'''


class Emitter(pygame.sprite.Sprite):
    def __init__(self, pos, acc_mod):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(center=pos)
        self.bullets = []
        self.shot_timer = 0
        self.delay = SHOOTING_DELAY
        self.acc_mod = acc_mod
        self.level = 1

    def move(self, loc):
        self.rect.center = loc
        for bullet in self.bullets:
            bullet.move()
            if bullet.out_of_bounds():
                self.bullets.remove(bullet)

    def shoot(self, mods):
        pass

    def get_bullets(self) -> list:
        return self.bullets

    def update_timers(self, ms, mods):
        for bullet in self.bullets:
            bullet.update_timers(ms)
        self.shot_timer += ms
        if self.shot_timer >= self.delay:
            self.shoot(mods)
            self.shot_timer -= self.delay

    def level_up(self):
        self.level += 1

    def get_level(self) -> int:
        return self.level


class FireShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)

    def shoot(self, mods):
        bullet = Fireball(self.rect.center + vec(-50, 0), self.acc_mod, mods)
        self.bullets.append(bullet)
        print(f'Fire! Bullets fired: {len(self.bullets)}')


class LitShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)

    def shoot(self, mods):
        bullet = Lightning(self.rect.center, self.acc_mod, mods)
        self.bullets.append(bullet)
        print(f'Lit! Bullets lited: {len(self.bullets)}')


class IceShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)
        self.life_timer = 0
        self.delay = 1500
        self.proj_dur = 3000
        self.max_proj = 6

    def shoot(self, mods):
        bullet = Iceball(self.rect.center, self.acc_mod, mods)
        self.bullets.append(bullet)
        if len(self.bullets) > self.max_proj:
            self.bullets = self.bullets[1::]
        print(f'Ice! Bullets iced: {len(self.bullets)}')
