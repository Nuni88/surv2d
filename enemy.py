import os
import random
import pygame
from actor import Actor
from constants import WIDTH, HEIGHT, ACC, FPS, DISP_SCALE

vec = pygame.math.Vector2


class Enemy(Actor):
    def __init__(self, enemydata):
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

    def update(self, ppos):
        super().move()
        # Sets enemy movement and sprite relative to player position
        if self.pos.x > ppos.x:
            self.acc.x = -ACC * self.speed_mod
            self.surf = self.frame_left
        else:
            self.acc.x = ACC * self.speed_mod
            self.surf = self.frame_right

    def take_damage(self, amt) -> bool:
        if amt > 0:
            # print(f'Enemy took {amt} damage.')
            self.health -= amt
            if self.health <= 0:
                return True
        return False

    def get_name(self) -> str:
        return self.name


class FlyingEnemy(Enemy):
    def __init__(self, enemydata):
        super().__init__(enemydata)
        self.pos.y = HEIGHT * round(random.uniform(0.1, 0.7), 2)
        self.rect.center = self.pos

    def update(self, ppos):
        # Move toward player directly
        dx, dy = (ppos.x - self.pos.x, ppos.y - self.pos.y)
        stepx, stepy = (self.speed_mod * dx // FPS, self.speed_mod * dy // FPS)
        self.pos = vec(self.pos.x + stepx, self.pos.y + stepy)
        self.rect.center = self.pos

'''
class EnemyOne(Enemy):
    def __init__(self):
        path_left = os.path.join('images\\enemy1', 'enemy_left.gif')
        path_right = os.path.join('images\\enemy1', 'enemy_right.gif')
        super().__init__(pygame.image.load(path_left))
        self.frame_left = pygame.transform.scale_by(pygame.image.load(path_left), DISP_SCALE)
        self.frame_right = pygame.transform.scale_by(pygame.image.load(path_right), DISP_SCALE)
        self.name = 'EnemyOne'
        self.damage = 5
        self.speed_mod = round(random.uniform(0.35, 0.45), 2)
        self.health = 1600


class EnemyTwo(Enemy):
    def __init__(self):
        path_left = os.path.join('images\\enemy2', 'enemy_left.gif')
        path_right = os.path.join('images\\enemy2', 'enemy_right.gif')
        super().__init__(pygame.image.load(path_left))
        self.frame_left = pygame.transform.scale_by(pygame.image.load(path_left), DISP_SCALE)
        self.frame_right = pygame.transform.scale_by(pygame.image.load(path_right), DISP_SCALE)
        self.name = 'EnemyTwo'
        self.damage = 2
        self.speed_mod = round(random.uniform(0.5, 0.6), 2)
        self.health = 800


class EnemyThree(Enemy):
    def __init__(self):
        path_left = os.path.join('images\\enemy3', 'enemy_left.gif')
        path_right = os.path.join('images\\enemy3', 'enemy_right.gif')
        super().__init__(pygame.image.load(path_left))
        self.frame_left = pygame.transform.scale_by(pygame.image.load(path_left), DISP_SCALE)
        self.frame_right = pygame.transform.scale_by(pygame.image.load(path_right), DISP_SCALE)
        self.name = 'EnemyThree'
        self.damage = 8
        self.speed_mod = round(random.uniform(0.15, 0.25), 2)
        self.health = 2400
'''
