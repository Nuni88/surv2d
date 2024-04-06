import pygame
from projectile import Fireball, Iceball, Lightning, Katana
from constants import STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2

# Modifiable values
BASE_SHOT_DELAY = 1000
BASE_DIMS = (100, 100)
BGCOLOR = pygame.Color('black')
WEAPONTYPES = {
    'Fireball': Fireball,
    'Iceball': Iceball,
    'Lightning': Lightning,
    'Katana': Katana
}


class Shooter(pygame.sprite.Sprite):
    def __init__(self, pos, data):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.Surface(BASE_DIMS), DISP_SCALE)
        self.image.fill(BGCOLOR)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=pos)
        self.shot_timer = 0
        self.level = 1
        self.name = data['name']
        self.delay = BASE_SHOT_DELAY * data['delay_mod']
        self.nodes = data['nodes']
        self.proj_type = data['proj_type']
        self.max_proj = data['max_proj']
        self.carryover = 0
        self.bullets = pygame.sprite.Group()

    def update(self, loc, offset, time_update, mods, dist):
        self.rect.center = loc
        self.bullets.update(offset, time_update, dist)
        self.shot_timer += time_update

        if self.shot_timer >= self.delay:
            num_bullets = 1 + mods[STAT_STRS['PROJNUM']]['value'] + self.carryover
            max_proj = int(self.max_proj + mods[STAT_STRS['PROJNUM']]['value'])
            while num_bullets >= 1 and len(self.bullets) < max_proj:
                for node in self.nodes:
                    if num_bullets >= 1 and len(self.bullets) < max_proj:
                        self.shoot(mods, self.nodes[node])
                        num_bullets -= 1
            self.carryover = num_bullets
            self.shot_timer -= self.delay

    def shoot(self, mods, node):
        offset = vec(node['x'] * DISP_SCALE, node['y'] * DISP_SCALE)
        bullet = WEAPONTYPES[self.proj_type](self.rect.center + offset, mods)
        self.bullets.add(bullet)

    def get_bullets(self) -> pygame.sprite.Group:
        return self.bullets

    def level_up(self):
        self.level += 1

    def get_level(self) -> int:
        return self.level

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)
