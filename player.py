import pygame
from pygame.locals import *
from emitter import FireShooter, LitShooter, IceShooter
from actor import Actor
from constants import WIDTH, HEIGHT, STAT_STRS, ACC, FRIC, DISP_SCALE

vec = pygame.math.Vector2

# Modifiable values
MOVE_EDGE_LEFT = WIDTH * 0.1
MOVE_EDGE_RIGHT = WIDTH * 0.9
GRAVITY = 0.9 * DISP_SCALE
JUMP_CANCEL_HT = -3 * DISP_SCALE


class Player(Actor):
    def __init__(self, chardata):
        super().__init__(pygame.image.load(chardata['frame_left']))
        self.pos = vec((WIDTH / 2, HEIGHT * 0.94))
        self.rect.midbottom = self.pos

        self.stats = chardata['stats']
        self.mods = chardata['mods']
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

        self.shooters = pygame.sprite.Group()
        shooter1 = FireShooter(self.rect.center, vec(1, 1))
        shooter2 = LitShooter(self.rect.center, vec(1, 1))
        shooter3 = IceShooter(self.rect.center, vec(1, 1))
        self.shooters.add(shooter1)
        self.shooters.add(shooter2)
        self.shooters.add(shooter3)

        # self.jump_sfx = pygame.mixer.Sound(os.path.join('sound', 'jump.wav'))
        # self.jump_sfx.set_volume(0.1)

    def update(self, time_update):
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
            if self.dodge_timer >= self.stats[STAT_STRS['DODGE']]['value'] * 1000:
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

        self.shooters.update(self.rect.center, self.get_scroll_dist(), time_update, self.mods)

    def move_x(self):
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
        self.pos.x += self.vel.x + self.acc.x * 0.5

        if self.pos.x < MOVE_EDGE_LEFT:
            self.pos.x = MOVE_EDGE_LEFT
        elif self.pos.x > MOVE_EDGE_RIGHT:
            self.pos.x = MOVE_EDGE_RIGHT

        self.rect.midbottom = self.pos

    def move_y(self):
        self.acc.y = GRAVITY
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + self.acc.y * 0.5

        self.rect.midbottom = self.pos

    def handle_collision_x(self, plat):
        # Moving left
        if self.vel.x < 0:
            self.rect.left = plat.rect.right
        # Moving right
        elif self.vel.x > 0:
            self.rect.right = plat.rect.left
        self.vel.x = 0
        self.pos = vec(self.rect.midbottom)

    def handle_collision_y(self, plat):
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

    def cancel_jump(self):
        if self.jumping and self.vel.y < JUMP_CANCEL_HT:
            self.vel.y = JUMP_CANCEL_HT

    def dodge(self):
        if not self.dodging and not self.jumping:
            print('Dodged!')
            self.dodging = True
            self.invincible = True

    def take_hit(self, enemy):
        if enemy.damage > 0:
            if not self.invincible:
                print(f'Took {enemy.damage} damage.')
                self.health -= enemy.damage
                if self.health <= 0:
                    self.kill()
                self.invincible = True

    def get_bullets(self) -> pygame.sprite.Group:
        bullets = pygame.sprite.Group()
        for shooter in self.shooters:
            for bullet in shooter.get_bullets():
                bullets.add(bullet)
        return bullets

    def get_scroll_dist(self) -> float:
        if not (MOVE_EDGE_LEFT < self.pos.x < MOVE_EDGE_RIGHT):
            return self.vel.x + self.acc.x * 0.5
        else:
            return 0

    def gain_stat_bonus(self, stat, amt):
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
            self.heal(amt)

    def heal(self, amt):
        if amt > 0:
            self.health += amt
        if self.health > self.stats[STAT_STRS['MAXHP']]['value']:
            self.health = self.stats[STAT_STRS['MAXHP']]['value']

    def heal_percent(self, mod):
        if mod > 0:
            self.health += int(self.stats[STAT_STRS['MAXHP']]['value'] * mod)
        if self.health > self.stats[STAT_STRS['MAXHP']]['value']:
            self.health = self.stats[STAT_STRS['MAXHP']]['value']

    def has_req_weapon(self, req, lvl) -> bool:
        for shooter in self.shooters:
            if shooter.__class__.__name__ == req and shooter.get_level() >= lvl:
                return True
        return False

    def has_req_stat(self, req, lvl) -> bool:
        if req in self.stats:
            if self.stats[req]['level'] >= lvl:
                return True
        elif req in self.mods:
            if self.mods[req]['level'] >= lvl:
                return True
        return False

    def get_max_health(self) -> int:
        return self.stats[STAT_STRS['MAXHP']]['value']

    def get_crit_chance(self) -> int:
        return self.stats[STAT_STRS['CRITC']]['value']

    def get_crit_mod(self) -> float:
        return self.mods[STAT_STRS['CRITD']]['value']

    def get_stats(self) -> dict:
        stats = self.stats
        for mod in self.mods:
            stats[mod] = self.mods[mod]
        return stats
