import pygame
from projectile import Fireball, Iceball, Lightning
from constants import DISP_SCALE

vec = pygame.math.Vector2
'''
WEAPONTYPES = {
    'Fireball': Fireball,
    'Iceball': Iceball,
    'Lightning': Lightning
}
'''
# Modifiable values
BASE_SHOT_DELAY = 1000
BASE_DIMS = (100, 100)  # (W, H)
BGCOLOR = pygame.Color('black')

# TODO: Read weapon attributes from file


class Emitter(pygame.sprite.Sprite):
    def __init__(self, pos, acc_mod):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.Surface(BASE_DIMS), DISP_SCALE)
        self.image.fill(BGCOLOR)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.shot_timer = 0
        self.delay = BASE_SHOT_DELAY
        self.acc_mod = acc_mod
        self.level = 1
        self.bullets = pygame.sprite.Group()

    def update(self, loc, offset, time_update, mods):
        self.rect.center = loc
        self.bullets.update(offset, time_update)
        self.shot_timer += time_update
        if self.shot_timer >= self.delay:
            self.shoot(mods)
            self.shot_timer -= self.delay

    def shoot(self, mods):
        pass

    def get_bullets(self) -> pygame.sprite.Group:
        return self.bullets

    def level_up(self):
        self.level += 1

    def get_level(self) -> int:
        return self.level

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)


class FireShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)
        self.max_proj = 6

    def shoot(self, mods):
        bullet = Fireball(self.rect.center + vec(-50, 0), self.acc_mod, mods)
        self.bullets.add(bullet)


class LitShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)
        self.max_proj = 6

    def shoot(self, mods):
        bullet = Lightning(self.rect.center, self.acc_mod, mods)
        self.bullets.add(bullet)


class IceShooter(Emitter):
    def __init__(self, pos, acc_mod):
        super().__init__(pos, acc_mod)
        self.life_timer = 0
        self.delay = 1500
        self.proj_dur = 3000
        self.max_proj = 6

    def shoot(self, mods):
        bullet = Iceball(self.rect.center, self.acc_mod, mods)
        self.bullets.add(bullet)
