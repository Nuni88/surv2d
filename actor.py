import pygame
import os
import random
from pygame.locals import *
from emitter import FireShooter, LitShooter, IceShooter
from constants import ACC, FRIC, WIDTH, HEIGHT, MOVE_EDGE_LEFT, MOVE_EDGE_RIGHT, GRAVITY,\
                      MAXHP, CRITC, CRITD, MSPD, JUMPH, INVUL

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.surf = surf
        self.rect = self.surf.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.health = 2500

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

    def get_pos(self) -> (float, float):
        return self.rect.midbottom


class Player(Actor):
    def __init__(self, chardata):
        super().__init__(pygame.image.load(chardata['frame_left']))
        self.pos = vec((WIDTH / 2, HEIGHT - 25))
        self.rect.midbottom = self.pos

        self.stats = chardata['stats']
        self.mods = chardata['mods']
        self.frame_left = chardata['frame_left']
        self.frame_right = chardata['frame_right']
        self.health = self.stats[MAXHP]
        # self.level = 1
        # self.exp = 0

        self.jumping = False
        self.midair_jumping = False
        self.invincible = False
        self.invul_timer = 0

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
            self.acc.x = -ACC * self.stats[MSPD]
            self.surf = pygame.image.load(self.frame_left)
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC * self.stats[MSPD]
            self.surf = pygame.image.load(self.frame_right)
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
            shooter.shoot(self.mods)

    def land(self, plat):
        # Player is below platform
        if self.rect.top >= plat.rect.top:
            self.rect.top = plat.rect.bottom + 1
            self.vel.y = -self.vel.y
        # Player is above platform
        elif self.vel.y > 0:
            self.pos.y = plat.rect.top
            self.vel.y = 0
            self.jumping = False
            self.midair_jumping = False

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vel.y = -self.stats[JUMPH]
            # self.jump_sfx.play()

    def midair_jump(self):
        if not self.midair_jumping:
            self.midair_jumping = True
            self.vel.y = -self.stats[JUMPH] / 2
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
        # Invulnerability wears off after InvulDuration seconds
        # Turn player invincibility off and reset invulnerability tracking
        if self.invincible:
            self.invul_timer += ms
            if self.invul_timer >= self.stats[INVUL] * 1000:
                self.invincible = False
                self.invul_timer = 0
        for shooter in self.shooters:
            shooter.update_timers(ms, self.mods)

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

    def get_scroll_dist(self) -> float:
        return self.vel.x + 0.5 * self.acc.x

    '''
    def gain_exp(self, amt) -> bool:
        self.exp += amt
        print(f'Player XP: {self.exp}')
        if self.exp >= 100:
            print('Level up!')
            self.level += 1
            self.exp -= 100
            return True
        return False
    '''

    def gain_stat_bonus(self, stat, amt):
        if stat in self.stats:
            self.stats[stat] += amt
        elif stat in self.mods:
            self.mods[stat] += amt
        print(f'Player {stat} went up by {amt}!')
        if stat == MAXHP:
            self.heal(amt)

    def heal(self, amt):
        if amt > 0:
            self.health += amt
        if self.health > self.stats[MAXHP]:
            self.health = self.stats[MAXHP]

    def heal_percent(self, mod):
        if mod > 0:
            self.health += int(self.stats[MAXHP] * mod)
        if self.health > self.stats[MAXHP]:
            self.health = self.stats[MAXHP]

    '''
    def get_level(self) -> int:
        return self.level

    def get_exp(self) -> int:
        return self.exp
    '''

    def get_max_health(self) -> int:
        return self.stats[MAXHP]

    def get_crit_chance(self) -> int:
        return self.stats[CRITC]

    def get_crit_mod(self) -> float:
        return self.mods[CRITD]


class Enemy(Actor):
    def __init__(self, surf):
        super().__init__(surf)

        # Spawn randomly on left or right side
        side = random.randint(0, 1)
        if side:
            x = random.randint(int(WIDTH * 1.5), int(WIDTH * 2))
        else:
            x = random.randint(int(WIDTH * -1), int(WIDTH * -0.5))
        self.pos = vec(x, HEIGHT - 25)
        self.rect.midbottom = self.pos
        self.name = ''

    def move_to(self, player):
        super().move()
        # Sets enemy movement and sprite relative to player position
        if self.pos.x > player.pos.x:
            self.acc.x = -ACC * self.speed_mod
            self.surf = self.spr_left
        else:
            self.acc.x = ACC * self.speed_mod
            self.surf = self.spr_right

    def take_damage(self, amt) -> bool:
        if amt > 0:
            print(f'Enemy took {amt} damage.')
            self.health -= amt
            if self.health <= 0:
                return True
        return False

    def get_name(self) -> str:
        return self.name


class EnemyOne(Enemy):
    def __init__(self):
        self.spr_left = pygame.image.load(os.path.join('images\\enemy1', 'enemy_left.gif'))
        self.spr_right = pygame.image.load(os.path.join('images\\enemy1', 'enemy_right.gif'))
        super().__init__(self.spr_left)
        self.name = 'EnemyOne'
        self.damage = 5
        self.speed_mod = round(random.uniform(0.35, 0.45), 2)
        self.health = 1600


class EnemyTwo(Enemy):
    def __init__(self):
        self.spr_left = pygame.image.load(os.path.join('images\\enemy2', 'enemy_left.gif'))
        self.spr_right = pygame.image.load(os.path.join('images\\enemy2', 'enemy_right.gif'))
        super().__init__(self.spr_left)
        self.name = 'EnemyTwo'
        self.damage = 2
        self.speed_mod = round(random.uniform(0.5, 0.6), 2)
        self.health = 800


class EnemyThree(Enemy):
    def __init__(self):
        self.spr_left = pygame.image.load(os.path.join('images\\enemy3', 'enemy_left.gif'))
        self.spr_right = pygame.image.load(os.path.join('images\\enemy3', 'enemy_right.gif'))
        super().__init__(self.spr_left)
        self.name = 'EnemyThree'
        self.damage = 8
        self.speed_mod = round(random.uniform(0.15, 0.25), 2)
        self.health = 2400
