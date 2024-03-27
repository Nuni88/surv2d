import sys
import time
import random
import os
import json
import pygame
from pygame.locals import *
from enemy import Enemy
from player import Player
from platform import Platform
from door import WeapDoor, StatDoor
from pickup import ExpPickup, ExpSmall, ExpMed, ExpLarge, MaxHealthPickup, HealthPickup
from menu import Menu
from cursor import Cursor
from constants import WIDTH, HEIGHT, FONT, STAT_STRS, DISP_SCALE

vec = pygame.math.Vector2

LOOT_TABLE = {
    'EnemyOne': ExpSmall,
    'EnemyTwo': ExpMed,
    'EnemyThree': ExpLarge
}

# Modifiable values
FPS = 60
MAX_TIME = 300
SPAWN_DELAY = 2000
FONT_SZ = 24
PLAT_RANGE = 20
BASE_EXP_REQ = 100
EXP_REQ_SCALE = 20
NUM_LVL_OPTIONS = 6
POT_DROP_RT = 10
TEXTBOXHT = 30
END_SCRN_COLOR = (255, 0, 0)   # (R, G, B)
BGCOLOR = (200, 200, 200)
TEXTCOLOR = (0, 0, 0)
STATS = []
for stat in STAT_STRS:
    STATS.append(STAT_STRS[stat])
LEVEL_BONUSES = {
    STAT_STRS['MAXHP']: 10,
    STAT_STRS['CRITC']: 0.05,
    STAT_STRS['ASPD']: 0.05,
    STAT_STRS['MSPD']: 0.05,
    STAT_STRS['JUMPH']: 1,
    STAT_STRS['DODGE']: -0.05,
    STAT_STRS['INVUL']: 0.01,
    STAT_STRS['DMG']: 0.05,
    STAT_STRS['CRITD']: 0.1,
    STAT_STRS['PROJSPD']: 0.05,
    STAT_STRS['PROJSZ']: 2.0,
    STAT_STRS['PROJNUM']: 0.1
}
PAUSE_MENU_OPTIONS = [
    'Resume',
    'Display Settings',
    'Controls',
    'Return to Title',
    'Quit'
]


# noinspection PyTypeChecker
class SurvGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Survivors")
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT, FONT_SZ)
        self.spawn_delay = SPAWN_DELAY
        self.level_up_menu = None
        self.pause_menu = None
        self.cursor = Cursor()
        self.time_delay = 0

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.actors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()

        # Add player data from JSON file and create player object
        unitdatafile = open(os.path.join('data', 'unitdata.json'), 'r')
        unitdata = json.loads(str(unitdatafile.read()))
        unitdatafile.close()
        self.P1 = Player(unitdata['Char1'])
        self.p_exp = 0
        self.p_level = 1
        self.to_next_level = BASE_EXP_REQ

        # Add enemy data from JSON file for spawning enemies
        enemydatafile = open(os.path.join('data', 'enemydata.json'), 'r')
        self.enemydata = json.loads(str(enemydatafile.read()))
        enemydatafile.close()

        # Generate platforms, walls, and doors
        self.floor = Platform(vec(WIDTH * 0.5, HEIGHT), 'plat_floor.png')
        self.platforms.add(self.floor)
        self.all_sprites.add(self.floor)
        for i in range(-PLAT_RANGE, PLAT_RANGE):
            plat = Platform(vec(WIDTH * (i - 0.5), HEIGHT * 0.65), 'plat_med.png')
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            plat = Platform(vec(WIDTH * i, HEIGHT * 0.77), 'plat_med.png')
            self.all_sprites.add(plat)
            self.platforms.add(plat)

        for i in range(-PLAT_RANGE, PLAT_RANGE):
            plat = Platform(vec(WIDTH * (i - 0.13), HEIGHT * 0.85), 'wall_med.png')
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            roll = random.randint(0, len(STATS) - 1)
            if i == 1:
                door = WeapDoor(vec(WIDTH * (i + 0.13), HEIGHT * 0.85), 'door.png', 'FireShooter', 2)
            else:
                door = StatDoor(vec(WIDTH * (i + 0.13), HEIGHT * 0.85), 'door.png', STATS[roll], 2)
            self.all_sprites.add(door)
            self.doors.add(door)
            self.platforms.add(door)

        heart = MaxHealthPickup(vec(WIDTH * 0.2, HEIGHT * 0.93))
        self.all_sprites.add(heart)
        self.pickups.add(heart)

        self.all_sprites.add(self.P1)
        self.actors.add(self.P1)

        pygame.mouse.set_visible(False)

    def spawn_enemy(self, enemy_type):
        enemy = enemy_type()
        self.all_sprites.add(enemy)
        self.actors.add(enemy)
        self.enemies.add(enemy)

    def spawn_enemies(self):
        for enemy in self.enemydata:
            e = Enemy(self.enemydata[enemy])
            self.all_sprites.add(e)
            self.actors.add(e)
            self.enemies.add(e)

    def add_level_up_menu(self):
        self.p_level += 1
        self.p_exp -= self.to_next_level
        self.to_next_level += EXP_REQ_SCALE
        options = []
        opts_len = len(STATS)
        while len(options) < NUM_LVL_OPTIONS:
            roll = random.randint(0, opts_len - 1)
            if STATS[roll] not in options:
                options.append(STATS[roll])
                print(f'{STATS[roll]}')
        self.level_up_menu = Menu(options, vec(self.displaysurface.get_rect().center))
        self.menu_sprites.add(self.level_up_menu)
        self.menu_sprites.add(self.cursor)

    def add_pause_menu(self):
        self.pause_menu = Menu(PAUSE_MENU_OPTIONS, vec(self.displaysurface.get_rect().center))
        self.menu_sprites.add(self.pause_menu)
        self.menu_sprites.add(self.cursor)

    def handle_pause_option(self, option):
        if option == '':
            return
        if option == 'Resume':
            self.pause_menu.kill()
            self.pause_menu = None
            self.cursor.kill()
            return
        if option == 'Display Settings':
            self.show_display_settings()
            return
        if option == 'Return to Title':
            self.end_game()
        if option == 'Quit':
            pygame.quit()
            sys.exit()

    def show_display_settings(self):
        pass

    def end_game(self):
        for entity in self.all_sprites:
            entity.kill()
        time.sleep(1)
        self.displaysurface.fill(END_SCRN_COLOR)
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    def run(self):
        spawn_timer = 0

        while True:
            time_update = self.clock.tick(FPS)

            # Pause menu open
            if self.pause_menu:
                self.time_delay += time_update
                self.cursor.move()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        # Left click
                        if event.button == 1:
                            menu_hit = pygame.sprite.collide_rect(self.cursor, self.pause_menu)
                            if menu_hit:
                                option = self.pause_menu.get_option(self.cursor)
                                self.handle_pause_option(option)
            else:
                if self.P1.get_health() <= 0:
                    return
                bullets = self.P1.get_bullets()

                if self.level_up_menu:
                    self.time_delay += time_update
                    self.cursor.move()
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == MOUSEBUTTONDOWN:
                            # Left click
                            if event.button == 1:
                                menu_hit = pygame.sprite.collide_rect(self.cursor, self.level_up_menu)
                                if menu_hit:
                                    option = self.level_up_menu.get_option(self.cursor)
                                    print(option)
                                    if option != '':
                                        self.P1.gain_stat_bonus(option, LEVEL_BONUSES[option])
                                        self.level_up_menu.kill()
                                        self.level_up_menu = None
                                        self.cursor.kill()
                else:
                    self.P1.move()
                    for enemy in self.enemies:
                        enemy.move_to(self.P1)

                    # Scroll the screen
                    if self.P1.out_of_bounds():
                        mod = self.P1.get_scroll_dist()
                        for enemy in self.enemies:
                            enemy.scroll(mod)
                        for bullet in bullets:
                            bullet.scroll(mod)
                        for pickup in self.pickups:
                            pickup.scroll(mod)
                        for plat in self.platforms:
                            plat.scroll(mod)

                    # Handle player grabbing pickups
                    pickup_hits = pygame.sprite.spritecollide(self.P1, self.pickups, False)
                    if pickup_hits:
                        for pickup in pickup_hits:
                            if isinstance(pickup, ExpPickup):
                                self.p_exp += pickup.get_value()
                                if self.p_exp >= self.to_next_level:
                                    self.add_level_up_menu()
                            else:
                                pickup.collect(self.P1)
                            pickup.kill()

                    # Handle opening locked doors
                    door_hits = pygame.sprite.spritecollide(self.P1, self.doors, False)
                    if door_hits:
                        for door in door_hits:
                            if door.unlockable(self.P1):
                                door.kill()

                    # Handle player landing
                    plat_hits = pygame.sprite.spritecollide(self.P1, self.platforms, False)
                    if plat_hits:
                        # self.P1.handle_platform_collision(plat_hits[0])
                        for plat in plat_hits:
                            self.P1.handle_platform_collision(plat)

                    # Handle damage from enemies
                    enemy_hits = pygame.sprite.spritecollide(self.P1, self.enemies, False)
                    if enemy_hits:
                        self.P1.take_hit(enemy_hits[0])

                    # Handle player shooting enemies
                    for bullet in bullets:
                        proj_hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
                        for enemy in proj_hits:
                            crit_chance = self.P1.get_crit_chance()
                            crit_mod = self.P1.get_crit_mod()
                            if enemy.take_damage(bullet.get_damage(crit_chance, crit_mod)):
                                print('Enemy killed!')
                                enemy_pos = enemy.get_pos()
                                hp_chance = random.randint(1, 100)
                                if hp_chance <= POT_DROP_RT:
                                    drop = HealthPickup(enemy_pos)
                                else:
                                    loot_type = LOOT_TABLE[enemy.get_name()]
                                    drop = loot_type(enemy_pos)
                                self.all_sprites.add(drop)
                                self.pickups.add(drop)
                                enemy.kill()

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                if plat_hits:
                                    self.P1.jump()
                                else:
                                    self.P1.midair_jump()
                            if event.key == pygame.K_r:
                                if plat_hits:
                                    self.P1.dodge()
                            if event.key == pygame.K_p:
                                self.add_pause_menu()
                            if event.key == pygame.K_ESCAPE:
                                return
                        '''
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_f:
                                self.P1.shoot()
                        '''
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_SPACE:
                                self.P1.cancel_jump()

                    self.floor.recenter(self.P1)

                    # Update timers
                    self.P1.update_timers(time_update)
                    spawn_timer += time_update
                    if spawn_timer >= self.spawn_delay:
                        self.spawn_enemies()
                        spawn_timer -= self.spawn_delay

                    # Check if time is over
                    game_time = MAX_TIME - int((pygame.time.get_ticks() - self.time_delay) / 1000)
                    print(f'Delay: {self.time_delay}')
                    if game_time == 0:
                        return

            self.displaysurface.fill(BGCOLOR)

            # Display timer as MM:SS
            minutes = int(game_time / 60)
            seconds = int(game_time - minutes * 60)
            if minutes < 10:
                minutes = '0' + str(minutes)
            if seconds < 10:
                seconds = '0' + str(seconds)

            text_time = self.font.render(f'Time: {minutes}:{seconds}', False, TEXTCOLOR)
            text_time = pygame.transform.scale_by(text_time, DISP_SCALE)
            hp = self.P1.get_health()
            mhp = self.P1.get_max_health()
            text_health = self.font.render(f'Health: {hp}/{mhp}', False, TEXTCOLOR)
            text_health = pygame.transform.scale_by(text_health, DISP_SCALE)
            level_pct = round(100 * self.p_exp / self.to_next_level, 2)
            text_level = self.font.render(f'Level: {self.p_level} [{level_pct}%]', False, TEXTCOLOR)
            text_level = pygame.transform.scale_by(text_level, DISP_SCALE)

            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for bullet in bullets:
                self.displaysurface.blit(bullet.surf, bullet.rect)
            for door in self.doors:
                door.display_lock()
            self.displaysurface.blit(text_time, (0, 0))
            self.displaysurface.blit(text_health, (0, TEXTBOXHT * DISP_SCALE))
            self.displaysurface.blit(text_level, (0, 2 * TEXTBOXHT * DISP_SCALE))
            if self.level_up_menu:
                for entity in self.menu_sprites:
                    self.displaysurface.blit(entity.surf, entity.rect)
                self.level_up_menu.display()
            elif self.pause_menu:
                for entity in self.menu_sprites:
                    self.displaysurface.blit(entity.surf, entity.rect)
                self.pause_menu.display()

            pygame.display.update()


if __name__ == '__main__':
    mygame = SurvGame()
    mygame.run()
    mygame.end_game()
