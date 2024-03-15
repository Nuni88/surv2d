import pygame
import os
import random
from pygame.locals import *
from emitter import FireShooter, LitShooter, IceShooter
from constants import ACC, FRIC, WIDTH, HEIGHT, MOVE_EDGE_LEFT, MOVE_EDGE_RIGHT, GRAVITY

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.surf = surf
        self.rect = self.surf.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 5000
        self.speed_mod = 1

    def pos_greater_x(self, other):
        return self.pos.x > other.pos.x

    def move(self):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def get_health(self) -> int:
        return self.health

    def scroll(self, offset):
        self.pos.x -= offset
        self.rect.midbottom = self.pos


class Player(Actor):
    def __init__(self):
        super().__init__(pygame.image.load(os.path.join('images\\player', 'player_right.gif')))
        self.pos = vec((WIDTH / 2, HEIGHT - 25))
        self.rect.midbottom = self.pos
        self.jumping = False
        self.midair_jumping = False
        self.invincible = False
        self.invul_dur = 2000
        self.invul_timer = 0
        self.health = 1000
        self.shooters = []
        shooter1 = FireShooter(self.rect.center, vec(1, 1))
        shooter2 = LitShooter(self.rect.topright, vec(1, 1))
        shooter3 = IceShooter(self.rect.bottomright, vec(1, 1))
        self.shooters.append(shooter1)
        self.shooters.append(shooter2)
        self.shooters.append(shooter3)

        # self.jump_sfx = pygame.mixer.Sound(os.path.join('sound', 'jump.wav'))
        # self.jump_sfx.set_volume(0.1)

    def move(self):
        self.acc = vec(0, GRAVITY)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\player', 'player_left.gif'))
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\player', 'player_right.gif'))
        self.shooters[0].move(self.rect.center)
        self.shooters[1].move(self.rect.topright)
        self.shooters[2].move(self.rect.bottomright)

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.scroll_left():
            self.pos.x = MOVE_EDGE_LEFT
        elif self.scroll_right():
            self.pos.x = MOVE_EDGE_RIGHT

        self.rect.midbottom = self.pos

    def shoot(self):
        for shooter in self.shooters:
            shooter.shoot()

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

    def take_hit(self, enemy):
        if enemy.damage > 0:
            if not self.invincible:
                print(f'Took {enemy.damage} damage.')
                self.health -= enemy.damage
                self.invincible = True

    def get_bullets(self) -> list:
        bullets = []
        for shooter in self.shooters:
            for bullet in shooter.get_bullets():
                bullets.append(bullet)
        return bullets

    def update_timers(self, ms):
        # Invincibility wears off after invul_dur time
        # Turn player invincibility off and reset invulnerability tracking
        if self.invincible:
            self.invul_timer += ms
            if self.invul_timer >= self.invul_dur:
                self.invincible = False
                self.invul_timer = 0
        for shooter in self.shooters:
            shooter.update_timers(ms)

    def scroll_left(self) -> bool:
        if self.pos.x < MOVE_EDGE_LEFT:
            return True
        return False

    def scroll_right(self) -> bool:
        if self.pos.x > MOVE_EDGE_RIGHT:
            return True
        return False

    def out_of_bounds(self) -> bool:
        if MOVE_EDGE_LEFT < self.pos.x < MOVE_EDGE_RIGHT:
            return False
        return True

    def get_scroll_modifier(self) -> float:
        return self.vel.x + 0.5 * self.acc.x


class Enemy(Actor):
    def __init__(self):
        super().__init__(pygame.image.load(os.path.join('images\\enemy1', 'enemy_left.gif')))
        self.pos = vec(random.randint(int(2 * WIDTH / 3), WIDTH - 10), HEIGHT - 25)
        self.rect.midbottom = self.pos
        self.damage = 10
        self.speed_mod = 0.8

    def set_facing(self, direction):
        if direction:
            self.acc.x = -ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\enemy1', 'enemy_left.gif'))
        else:
            self.acc.x = ACC * self.speed_mod
            self.surf = pygame.image.load(os.path.join('images\\enemy1', 'enemy_right.gif'))

    def take_damage(self, amt):
        if amt > 0:
            print(f'Enemy took {amt} damage.')
            self.health -= amt
