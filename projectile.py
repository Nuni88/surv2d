import os
import math
import random
import pygame
from constants import WIDTH, HEIGHT, STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2

# TODO: Read projectile attributes from file
# Modifiable values
ACC_ANGLE = math.pi


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, acc_mod, image, scale):
        super().__init__()
        self.image = pygame.transform.scale_by(image, scale * DISP_SCALE)
        self.rect = self.image.get_rect(center=pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.acc.x *= acc_mod.x
        self.acc.y *= acc_mod.y
        self.timer = 0
        self.damage = 0
        self.crit = 0
        self.duration = 0
        self.dur_timer = 0

    def update(self, offset, time_update):
        # Projectile lasts for limited time
        self.dur_timer += time_update
        if self.dur_timer > self.duration:
            self.kill()
            return

        self.rect.centerx -= offset
        self.timer += time_update
        self.vel += self.acc
        self.rect.center += self.vel
        self.check_bounds()

    def check_bounds(self):
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
        elif self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def get_damage(self, crit_chance, crit_mod) -> int:
        roll = random.randint(0, 99)
        if roll < crit_chance + self.crit:
            # print('Critical hit!')
            return int(self.damage * crit_mod)
        return self.damage

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)


class Fireball(Projectile):
    def __init__(self, pos, acc_mod, mods):
        image = pygame.image.load(os.path.join('images\\projectiles', 'fire.png'))
        super().__init__(pos, acc_mod, image, mods[STAT_STRS['PROJSZ']]['value'])
        self.acc_angle = ACC_ANGLE
        self.acc = vec(0, -0.1)
        self.vel = vec(0, -0.1)
        self.damage = int(1 * mods[STAT_STRS['DMG']]['value'])
        self.crit = 20
        self.speed_mod = 0.001
        self.rot_delay = 20
        self.degrees = 0
        self.duration = 8000

    def update(self, offset, time_update):
        super().update(offset, time_update)
        while self.timer >= self.rot_delay:
            self.degrees += 4
            self.timer -= self.rot_delay
        self.vel.rotate_ip(self.degrees)
        self.degrees = 0

    def move(self):
        self.vel += self.acc
        self.rect.center += self.vel


class Iceball(Projectile):
    def __init__(self, pos, acc_mod, mods):
        image = pygame.image.load(os.path.join('images\\projectiles', 'ice.png'))
        super().__init__(pos, acc_mod, image, mods[STAT_STRS['PROJSZ']]['value'])
        self.acc = vec(0, 0)
        self.damage = int(5 * mods[STAT_STRS['DMG']]['value'])
        self.crit = 0
        self.duration = 10000


class Lightning(Projectile):
    def __init__(self, pos, acc_mod, mods):
        image = pygame.image.load(os.path.join('images\\projectiles', 'lit.png'))
        super().__init__(pos, acc_mod, image, mods[STAT_STRS['PROJSZ']]['value'])
        self.acc = vec(0.1, 0.1)
        self.acc.x *= acc_mod.x
        self.acc.y *= acc_mod.y
        self.acc *= mods[STAT_STRS['PROJSPD']]['value']
        self.damage = int(2 * mods[STAT_STRS['DMG']]['value'])
        self.crit = 10
        self.wobble_delay = 200
        self.duration = 5000

    def update(self, offset, time_update):
        super().update(offset, time_update)
        if self.timer > self.wobble_delay:
            self.acc.y = -self.acc.y
            self.vel.y = -self.vel.y
            self.timer -= self.wobble_delay
