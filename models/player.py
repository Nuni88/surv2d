import pygame
import copy
from pygame.locals import *
from models.meleeweapon import FireWheel, KatanaW
from models.homingweapon import LitStrike
from models.staticweapon import IceMine
from models.actor import Actor
from models.enemy import Enemy
from models.obstacle import Obstacle
from globals.constants import WIDTH, HEIGHT, STAT_STRS, ACC, FRIC, DISP_SCALE

vec = pygame.math.Vector2

# Modifiable values
MOVE_EDGE_LEFT = int(WIDTH * 0.1)
MOVE_EDGE_RIGHT = int(WIDTH * 0.9)
GRAVITY = 0.9 * DISP_SCALE
JUMP_CANCEL_HT = -3 * DISP_SCALE
BASE_DODGE_CD = 5.0


class Player(Actor):
    def __init__(self, chardata: dict):
        try:
            if chardata is None:
                raise ValueError
            if type(chardata) is not dict:
                raise TypeError

        except (ValueError, TypeError) as e:
            raise

        else:
            super().__init__(pygame.image.load(chardata['frame_left']))
            self.pos = vec(int(WIDTH / 2), int(HEIGHT * 0.94))
            self.rect.midbottom = self.pos

            self.stats = copy.deepcopy(chardata['stats'])
            self.mods = copy.deepcopy(chardata['mods'])
            self.frame_left = pygame.transform.scale_by(pygame.image.load(chardata['frame_left']), DISP_SCALE)
            self.frame_right = pygame.transform.scale_by(pygame.image.load(chardata['frame_right']), DISP_SCALE)
            self.frame_dodge = pygame.transform.scale_by(pygame.image.load(chardata['frame_dodge']), DISP_SCALE)
            self.health = self.stats[STAT_STRS['MAXHP']]['value']

            self.jumping = False
            self.midair_jumping = False
            self.dodging = False
            self.dodge_timer = 0
            self.invincible = False
            self.invul_timer = 0
            self.last_pos = self.pos

            self.weapons = pygame.sprite.Group()
            # self.weapons.add(FireWheel(self.rect.center))
            self.weapons.add(KatanaW(self.rect.center))
            # self.weapons.add(LitStrike(self.rect.center))
            # self.weapons.add(IceMine(self.rect.center))

            # self.jump_sfx = pygame.mixer.Sound(os.path.join('sound', 'jump.wav'))
            # self.jump_sfx.set_volume(0.1)

    def update(self, time_update: int):
        try:
            if type(time_update) is not int:
                raise TypeError
            if time_update < 0:
                raise ValueError

        except (TypeError, ValueError) as e:
            raise

        else:
            if self.health <= 0:
                self.kill()
                return

            if self.dodging and self.invincible:
                self.image = self.frame_dodge
            # print(f'Player pos: {self.pos}')

            # Time between dodges determined by dodge stat
            # Turn dodge cooldown off and reset tracking
            if self.dodging:
                self.dodge_timer += time_update
                if self.dodge_timer >= (BASE_DODGE_CD - self.stats[STAT_STRS['DODGE']]['value']) * 1000:
                    self.dodging = False
                    self.dodge_timer = 0

            # Invulnerability wears off after seconds determined by invulnerability stat
            # Turn player invincibility off and reset invulnerability tracking
            if self.invincible:
                self.invul_timer += time_update
                if self.invul_timer >= self.stats[STAT_STRS['INVUL']]['value'] * 1000:
                    self.invincible = False
                    self.invul_timer = 0
                    if self.dodging:
                        self.image = self.frame_left

            self.weapons.update(self.rect.center, self.get_scroll_dist(), time_update, self.mods, self.pos - self.last_pos)

    def move_x(self):
        self.last_pos.x = self.pos.x
        self.acc.x = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC * self.stats[STAT_STRS['MSPD']]['value']
            self.image = self.frame_left
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC * self.stats[STAT_STRS['MSPD']]['value']
            self.image = self.frame_right

        self.acc.x += self.vel.x * FRIC
        self.vel.x += self.acc.x
        self.pos.x += int(self.vel.x + self.acc.x * 0.5)

        if self.pos.x < MOVE_EDGE_LEFT:
            self.pos.x = MOVE_EDGE_LEFT
        elif self.pos.x > MOVE_EDGE_RIGHT:
            self.pos.x = MOVE_EDGE_RIGHT

        self.rect.midbottom = self.pos

    def move_y(self):
        self.last_pos.y = self.pos.y
        self.acc.y = GRAVITY
        self.vel.y += self.acc.y
        self.pos.y += int(self.vel.y + self.acc.y * 0.5)

        self.rect.midbottom = self.pos

    def handle_collision_x(self, plat: Obstacle):
        try:
            if plat is None:
                raise ValueError
            if not isinstance(plat, Obstacle):
                raise TypeError

        except (ValueError, TypeError) as e:
            raise

        else:
            # Moving left
            if self.vel.x < 0:
                self.rect.left = plat.rect.right
            # Moving right
            elif self.vel.x > 0:
                self.rect.right = plat.rect.left
            self.vel.x = 0
            self.pos = vec(self.rect.midbottom)

    def handle_collision_y(self, plat: Obstacle):
        try:
            if plat is None:
                raise ValueError
            if not isinstance(plat, Obstacle):
                raise TypeError

        except (ValueError, TypeError) as e:
            raise

        else:
            # Moving up
            if self.vel.y < 0:
                self.rect.top = plat.rect.bottom
            # Moving down
            elif self.vel.y > 0:
                self.rect.bottom = plat.rect.top
                self.jumping = False
                self.midair_jumping = False
            self.vel.y = 0
            self.pos = vec(self.rect.midbottom)

    def jump(self):
        if not self.jumping:
            if self.vel.y == 0:
                self.jumping = True
                self.vel.y = -self.stats[STAT_STRS['JUMPH']]['value'] * DISP_SCALE
                # self.jump_sfx.play()
        elif not self.midair_jumping:
            self.midair_jumping = True
            self.vel.y = -self.stats[STAT_STRS['JUMPH']]['value'] * 0.5 * DISP_SCALE
            # self.jump_sfx.play()

    # TODO: Add tests
    def cancel_jump(self):
        if self.jumping and self.vel.y < JUMP_CANCEL_HT:
            self.vel.y = JUMP_CANCEL_HT

    # TODO: Add tests
    def dodge(self):
        if not self.dodging and not self.jumping:
            print('Dodged!')
            self.dodging = True
            self.invincible = True

    # TODO: Add tests
    def take_hit(self, enemy: Enemy):
        try:
            if not isinstance(enemy, Enemy):
                raise TypeError

        except TypeError as e:
            raise

        else:
            if enemy.damage > 0:
                if not self.invincible:
                    print(f'Took {enemy.damage} damage.')
                    self.health -= enemy.damage
                    if self.health <= 0:
                        self.kill()
                    self.invincible = True

    # TODO: Add tests
    def get_bullets(self) -> pygame.sprite.Group:
        bullets = pygame.sprite.Group()
        for shooter in self.weapons:
            for bullet in shooter.get_bullets():
                bullets.add(bullet)
        return bullets

    # TODO: Add tests
    def get_scroll_dist(self) -> float:
        if not (MOVE_EDGE_LEFT < self.pos.x < MOVE_EDGE_RIGHT):
            return self.vel.x + self.acc.x * 0.5
        else:
            return 0

    # TODO: Add tests
    def gain_stat_bonus(self, stat: str, amt: float):
        try:
            if type(stat) is not str or type(amt) is not float:
                raise TypeError
            if stat not in self.stats and stat not in self.mods:
                raise ValueError(f'{stat} not found')
            if amt <= 0:
                raise ValueError(f'Amount is {amt}. Should be > 0.')

        except (ValueError, TypeError) as e:
            raise

        else:
            if stat in self.stats:
                self.stats[stat]['value'] += amt
                self.stats[stat]['level'] += 1
                print(f'Player {stat} went up by {amt}!')
                print(f'{stat} is now level {self.stats[stat]["level"]}!')
            elif stat in self.mods:
                self.mods[stat]['value'] += amt
                self.mods[stat]['level'] += 1
                print(f'Player {stat} went up by {amt}!')
                print(f'{stat} is now level {self.mods[stat]["level"]}!')
            if stat == STAT_STRS['MAXHP']:
                self.heal(int(amt))
                self.stats[stat]['value'] = int(self.stats[stat]['value'])

    # TODO: Add tests
    def heal(self, amt: int):
        try:
            if type(amt) is not int:
                raise TypeError
            if amt <= 0:
                raise ValueError

        except (TypeError, ValueError) as e:
            raise

        else:
            self.health += amt
            if self.health > self.stats[STAT_STRS['MAXHP']]['value']:
                self.health = self.stats[STAT_STRS['MAXHP']]['value']

    def heal_percent(self, mod: float):
        try:
            if mod <= 0:
                raise ValueError
            if type(mod) is not float:
                raise TypeError

        except (ValueError, TypeError) as e:
            raise

        else:
            self.health += int(self.stats[STAT_STRS['MAXHP']]['value'] * mod)
            if self.health > self.stats[STAT_STRS['MAXHP']]['value']:
                self.health = self.stats[STAT_STRS['MAXHP']]['value']

    # TODO: Add tests
    def has_req_weapon(self, req: str, lvl: int) -> bool:
        try:
            if type(req) is not str or type(lvl) is not int:
                raise TypeError
            # if req not in weapon types
            #     raise ValueError
            if lvl < 0:
                raise ValueError

        except (TypeError, ValueError) as e:
            raise

        else:
            for shooter in self.weapons:
                if shooter.__class__.__name__ == req and shooter.get_level() >= lvl:
                    return True
            return False

    def has_req_stat(self, req: str, lvl: int) -> bool:
        try:
            if type(req) is not str or type(lvl) is not int:
                raise TypeError
            if req not in self.stats and req not in self.mods:
                raise ValueError
            if lvl < 0:
                raise ValueError

        except (TypeError, ValueError) as e:
            raise

        else:
            if req in self.stats:
                if self.stats[req]['level'] >= lvl:
                    return True
            elif req in self.mods:
                if self.mods[req]['level'] >= lvl:
                    return True
            return False

    def get_max_health(self) -> int:
        return self.stats[STAT_STRS['MAXHP']]['value']

    def get_crit_chance(self) -> float:
        return self.stats[STAT_STRS['CRITC']]['value']

    def get_crit_mod(self) -> float:
        return self.mods[STAT_STRS['CRITD']]['value']

    def get_pickup_range(self) -> float:
        return self.stats[STAT_STRS['PRANGE']]['value']

    def get_stats(self) -> dict:
        stats = self.stats
        for mod in self.mods:
            stats[mod] = self.mods[mod]
        return stats
