import pygame
from globals.constants import DISP_SCALE, FRIC

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface):
        try:
            if image is None:
                raise ValueError
            if not isinstance(image, pygame.surface.Surface):
                raise TypeError

        except (ValueError, TypeError) as e:
            raise

        else:
            super().__init__()
            self.image = pygame.transform.scale_by(image, DISP_SCALE)
            self.rect = self.image.get_rect()
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.pos = vec(0, 0)
            self.health = 0

    def pos_greater_x(self, other: pygame.sprite.Sprite):
        return self.pos.x > other.pos.x

    def move(self):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def get_health(self) -> int:
        return self.health

    def get_pos(self) -> tuple[float, float]:
        return self.rect.center

    def scale_to_screen(self, scale: float):
        try:
            if type(scale) is not float:
                raise TypeError

        except TypeError as e:
            raise

        else:
            self.image = pygame.transform.scale_by(self.image, scale)

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
