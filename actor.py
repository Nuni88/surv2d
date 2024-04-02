import pygame
from constants import DISP_SCALE, FRIC

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.surf = pygame.transform.scale_by(surf, DISP_SCALE)
        self.rect = self.surf.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 0

    def pos_greater_x(self, other):
        return self.pos.x > other.pos.x

    def move(self):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def get_health(self) -> int:
        return self.health

    def get_pos(self) -> (float, float):
        return self.rect.center

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)

    '''
    def handle_collision_x(self, plat):
        # Moving left
        if self.vel.x < 0:
            self.rect.left = plat.rect.right
        # Moving right
        elif self.vel.x > 0:
            self.rect.right = plat.rect.left
        self.vel.x = 0
        self.pos = vec(self.rect.midbottom)
    '''
