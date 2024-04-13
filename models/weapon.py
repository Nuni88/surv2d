import pygame
from models.projectile import Projectile
from models.constants import STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2

# Modifiable values
BASE_SHOT_DELAY = 1000
BASE_DIMS = (100, 100)
BGCOLOR = pygame.Color('black')


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.math.Vector2, ptype: Projectile, delay_mod: float):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.Surface(BASE_DIMS), DISP_SCALE)
        self.image.fill(BGCOLOR)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.shot_timer = 0
        self.level = 1
        self.proj_type = ptype
        self.delay = BASE_SHOT_DELAY * delay_mod
        self.nodes = []
        self.max_proj = 0
        self.carryover = 0
        self.bullets = pygame.sprite.Group()

    def update(self, loc: pygame.math.Vector2, offset: float, time_update: int, mods: dict, dist: pygame.math.Vector2):
        self.rect.center = loc
        self.bullets.update(offset, time_update, dist)
        self.shot_timer += time_update

        if self.shot_timer >= self.delay:
            num_bullets = 1 + mods[STAT_STRS['PROJNUM']]['value'] + self.carryover
            max_proj = int(self.max_proj + mods[STAT_STRS['PROJNUM']]['value'])
            while num_bullets >= 1 and len(self.bullets) < max_proj:
                for node in self.nodes:
                    if num_bullets >= 1 and len(self.bullets) < max_proj:
                        self.shoot(mods, node)
                        num_bullets -= 1
            self.carryover = num_bullets
            self.shot_timer -= self.delay

    def shoot(self, mods: dict, node: pygame.math.Vector2):
        bullet = self.proj_type(self.rect.center + node, mods)
        self.bullets.add(bullet)

    def get_bullets(self) -> pygame.sprite.Group:
        return self.bullets

    def level_up(self):
        self.level += 1

    def get_level(self) -> int:
        return self.level

    def scale_to_screen(self, scale: float):
        self.image = pygame.transform.scale_by(self.image, scale)
