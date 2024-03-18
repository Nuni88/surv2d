import os
import math
import random
import pygame
from constants import WIDTH, HEIGHT, ACC_ANGLE

vec = pygame.math.Vector2


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, acc_mod, surf, scale):
        super().__init__()
        self.surf = pygame.transform.scale_by(surf, scale)
        self.rect = self.surf.get_rect(center=pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.acc.x *= acc_mod.x
        self.acc.y *= acc_mod.y
        self.timer = 0
        self.damage = 0
        self.crit = 0

    def move(self):
        self.vel += self.acc
        self.rect.center += self.vel

    def update_timers(self, ms):
        self.timer += ms

    def out_of_bounds(self) -> bool:
        if self.rect.left > WIDTH or self.rect.right < 0:
            return True
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            return True
        return False

    def get_damage(self, crit_chance, crit_mod) -> int:
        roll = random.randint(0, 99)
        if roll < crit_chance + self.crit:
            print('Critical hit!')
            return int(self.damage * crit_mod)
        return self.damage

    def scroll(self, offset):
        self.rect.centerx -= offset


class Fireball(Projectile):
    def __init__(self, pos, acc_mod, mods):
        super().__init__(pos, acc_mod, pygame.image.load(os.path.join('images\\projectiles', 'fire.png')), mods['WeaponArea'])
        self.acc_angle = ACC_ANGLE
        self.acc = vec(0, -0.1)
        self.vel = vec(0, -0.1)
        self.damage = int(1 * mods['Damage'])
        self.crit = 20
        self.speed_mod = 0.001
        self.rot_delay = 20
        self.degrees = 0

    def update_timers(self, ms):
        super().update_timers(ms)
        while self.timer >= self.rot_delay:
            self.degrees += 4
            self.timer -= self.rot_delay
        self.vel.rotate_ip(self.degrees)
        self.degrees = 0
        '''
        while self.timer >= self.rot_delay:
            self.acc_angle += ACC_ANGLE
            self.timer -= self.rot_delay
        self.acc.x += self.speed_mod * math.cos(self.acc_angle)
        self.acc.y += -self.speed_mod * math.sin(self.acc_angle)
        '''

    def move(self):
        self.rect.center += self.vel

    def move(self):
        self.vel += self.acc
        self.rect.center += self.vel


class Iceball(Projectile):
    def __init__(self, pos, acc_mod, mods):
        super().__init__(pos, acc_mod, pygame.image.load(os.path.join('images\\projectiles', 'ice.png')), mods['WeaponArea'])
        self.acc = vec(0, 0)
        self.damage = int(5 * mods['Damage'])
        self.crit = 0


class Lightning(Projectile):
    def __init__(self, pos, acc_mod, mods):
        super().__init__(pos, acc_mod, pygame.image.load(os.path.join('images\\projectiles', 'lit.png')), mods['WeaponArea'])
        self.acc = vec(0.1, 0.1)
        self.acc.x *= acc_mod.x
        self.acc.y *= acc_mod.y
        self.acc *= mods['ProjSpeed']
        self.damage = int(2 * mods['Damage'])
        self.crit = 10

    def update_timers(self, ms):
        super().update_timers(ms)
        if self.timer > 200:
            self.acc.y = -self.acc.y
            self.vel.y = -self.vel.y
            self.timer -= 200
