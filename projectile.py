import os
import json
import random
import pygame
from constants import WIDTH, HEIGHT, STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2

# Modifiable values
bulletdatafile = open(os.path.join('data', 'bulletdata.json'), 'r')
BULLETDATA = json.loads(str(bulletdatafile.read()))
bulletdatafile.close()
BASE_IMG_PATH = 'images\\weapons'


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, mods, data):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_IMG_PATH, data['image']))
        self.image = pygame.transform.scale_by(image, mods[STAT_STRS['PROJSZ']]['value'] * DISP_SCALE)
        self.rect = self.image.get_rect(center=pos)
        self.vel = vec(data['v0_x'], data['v0_y'])
        self.acc = vec(data['a0_x'], data['a0_y'])
        self.acc *= mods[STAT_STRS['PROJSPD']]['value']
        self.crit = data['base_crit']
        self.damage = int(data['damage'] * mods[STAT_STRS['DMG']]['value'])
        self.duration = data['duration']
        self.dur_timer = 0

    def update(self, offset, time_update, dist):
        self.rect.centerx -= offset
        self.vel += self.acc
        self.rect.center += self.vel

    def check_bounds(self):
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
        elif self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def check_duration(self, time_update):
        self.dur_timer += time_update
        if self.dur_timer > self.duration:
            self.kill()

    def get_damage(self, crit_chance, crit_mod) -> int:
        roll = random.randint(0, 99)
        if roll < crit_chance + self.crit:
            # print('Critical hit!')
            return int(self.damage * crit_mod)
        return self.damage

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)

    def handle_collision(self) -> bool:
        pass


class Fireball(Projectile):
    def __init__(self, pos, mods):
        super().__init__(pos, mods, BULLETDATA['Fireball'])
        self.rot_delay = 120
        self.rot_timer = 0

    def update(self, offset, time_update, dist):
        super().update(offset, time_update, dist)
        self.rect.centerx += offset
        self.rect.center += dist
        self.rot_timer += time_update
        degrees = 0
        while self.rot_timer >= self.rot_delay:
            degrees += 6
            self.rot_timer -= self.rot_delay
        self.vel.rotate_ip(degrees)

    def move(self):
        self.vel += self.acc
        self.rect.center += self.vel


class Iceball(Projectile):
    def __init__(self, pos, mods):
        super().__init__(pos, mods, BULLETDATA['Iceball'])
        self.durability = 15

    def handle_collision(self):
        self.durability -= 1
        if self.durability <= 0:
            self.kill()


class Lightning(Projectile):
    def __init__(self, pos, mods):
        super().__init__(pos, mods, BULLETDATA['Lightning'])
        self.wobble_delay = 200
        self.wobble_timer = 0
        self.durability = 30

    def update(self, offset, time_update, dist):
        super().update(offset, time_update, dist)
        self.wobble_timer += time_update
        if self.wobble_timer > self.wobble_delay:
            self.acc.y = -self.acc.y
            self.vel.y = -self.vel.y
            self.wobble_timer -= self.wobble_delay
        self.check_bounds()
        self.check_duration(time_update)

    def handle_collision(self):
        self.durability -= 1
        if self.durability <= 0:
            self.kill()


class Katana(Projectile):
    def __init__(self, pos, mods):
        super().__init__(pos, mods, BULLETDATA['Katana'])

    def update(self, offset, time_update, dist):
        super().update(offset, time_update, dist)
        self.check_duration(time_update)
