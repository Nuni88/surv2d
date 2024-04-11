import os
import random
import pygame
from actor import Actor
from constants import WIDTH, HEIGHT, ACC, FPS, DISP_SCALE

vec = pygame.math.Vector2


class Enemy(Actor):
    def __init__(self, enemydata: dict):
        super().__init__(pygame.image.load(enemydata['frame_left']))
        self.frame_left = pygame.transform.scale_by(pygame.image.load(enemydata['frame_left']), DISP_SCALE)
        self.frame_right = pygame.transform.scale_by(pygame.image.load(enemydata['frame_right']), DISP_SCALE)
        self.name = enemydata['name']
        self.damage = enemydata['damage']
        self.speed_mod = round(random.uniform(enemydata['speed_mod'] - 0.05, enemydata['speed_mod'] + 0.05), 2)
        self.health = enemydata['health']

        # Spawn randomly on left or right side
        side = random.randint(0, 1)
        if side:
            x = random.randint(int(WIDTH * 1.5), int(WIDTH * 2))
        else:
            x = random.randint(int(WIDTH * -1), int(WIDTH * -0.5))
        self.pos = vec(x, HEIGHT * 0.95)
        self.rect.midbottom = self.pos

    def update(self, ppos: pygame.math.Vector2, offset: float):
        self.pos.x -= offset
        super().move()
        # Sets enemy movement and sprite relative to player position
        if self.pos.x > ppos.x:
            self.acc.x = -ACC * self.speed_mod
            self.image = self.frame_left
        else:
            self.acc.x = ACC * self.speed_mod
            self.image = self.frame_right

    def take_damage(self, amt: float):
        if amt > 0:
            # print(f'Enemy took {amt} damage.')
            self.health -= amt
            if self.health <= 0:
                print('Enemy killed!')
                self.kill()

    def get_name(self) -> str:
        return self.name

    '''
    def handle_collision_y(self, plat):
        # Moving up
        if self.vel.y < 0:
            self.rect.top = plat.rect.bottom
        # Moving down
        elif self.vel.y > 0:
            self.rect.bottom = plat.rect.top
        self.vel.y = 0
        self.pos = vec(self.rect.midbottom)
    '''


class GroundEnemy(Enemy):
    def __init__(self, enemydata: dict):
        super().__init__(enemydata)

    def update(self, ppos: pygame.math.Vector2, offset: float):
        super().update(ppos, offset)


class FlyingEnemy(Enemy):
    def __init__(self, enemydata: dict):
        super().__init__(enemydata)
        self.pos.y = HEIGHT * round(random.uniform(0.1, 0.7), 2)
        self.rect.center = self.pos

    def update(self, ppos: pygame.math.Vector2, offset: float):
        self.pos.x -= offset
        # Move toward player directly
        dx, dy = (ppos.x - self.pos.x, ppos.y - self.pos.y)
        self.vel = vec(self.speed_mod * dx / FPS, self.speed_mod * dy / FPS)
        self.pos += self.vel
        self.rect.center = self.pos
