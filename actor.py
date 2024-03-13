import pygame
import os
import random
from pygame.locals import *
from constants import ACC, FRIC, WIDTH, HEIGHT

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = None
        self.rect = None
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 20
        self.speed_mod = 1

    def pos_greater_x(self, other):
        return self.pos.x > other.pos.x

    def move(self):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def get_health(self) -> int:
        return self.health


class Player(Actor):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images\\player', 'player_right.gif'))
        self.rect = self.surf.get_rect()
        self.pos = vec((10, HEIGHT - 25))
        self.jumping = False
        self.midair_jumping = False
        self.invincible = False
        self.health = 50

        # self.jump_sfx = pygame.mixer.Sound(os.path.join('sound', 'jump.wav'))
        # self.jump_sfx.set_volume(0.1)

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\player', 'player_left.gif'))
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\player', 'player_right.gif'))

        super().move()

    def land(self, floor):
        if self.vel.y > 0:
            self.pos.y = floor
            self.vel.y = 0
            self.jumping = False
            self.midair_jumping = False

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vel.y = -15
            # self.jump_sfx.play()

    def midair_jump(self):
        if not self.midair_jumping:
            self.midair_jumping = True
            self.vel.y = -10
            # self.jump_sfx.play()

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

    def take_damage(self, amt) -> bool:
        if not self.invincible:
            print(f'Took {amt} damage.')
            self.health -= amt
            self.invincible = True
            return True
        return False

    def vulnerable(self):
        self.invincible = False


class Enemy(Actor):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images\\enemy1', 'enemy_left.gif'))
        self.rect = self.surf.get_rect()
        self.pos = vec(random.randint(WIDTH / 2, WIDTH - 10), HEIGHT - 25)
        self.damage = 10
        self.speed_mod = 0.8

    def set_facing(self, direction):
        if direction:
            self.acc.x = -ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\enemy1', 'enemy_left.gif'))
        else:
            self.acc.x = ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\enemy1', 'enemy_right.gif'))

    def get_damage(self) -> int:
        return self.damage
