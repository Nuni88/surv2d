import sys
import time
import random
import os
import json
import pygame
from pygame.locals import *
from models.enemy import GroundEnemy, FlyingEnemy
from models.player import Player
from models.obstacle import Obstacle
from models.door import WeapDoor, StatDoor
from models.pickup import ExpPickup, StatPickup, HealthPickup
from models.menu import Menu
from models.cursor import Cursor
from globals.constants import WIDTH, HEIGHT, FONT, STAT_STRS, FPS, DISP_SCALE, EVENTS

vec = pygame.math.Vector2

LOOT_TABLE = {
    'EnemyOne': 'ExpS',
    'EnemyTwo': 'ExpM',
    'EnemyThree': 'ExpL',
    'FlyingEnemyOne': 'ExpS'
}

# Modifiable values
MAX_TIME = 300
SPAWN_DELAY = 2000
FONT_SZ = 24
PLAT_RANGE = 20
BASE_EXP_REQ = 100
EXP_REQ_SCALE = 20
NUM_LVL_OPTIONS = 6
POT_DROP_RT = 10
TEXTBOXHT = 30 * DISP_SCALE
TEXTSTATHT = 20 * DISP_SCALE
END_SCRN_COLOR = pygame.Color('red3')
BGCOLOR = pygame.Color('darkseagreen3')
TEXTCOLOR = pygame.Color('black')
STATS = []
for stat in STAT_STRS:
    STATS.append(STAT_STRS[stat])
LEVEL_BONUSES = {
    STAT_STRS['MAXHP']: 10.0,
    STAT_STRS['CRITC']: 0.05,
    STAT_STRS['ASPD']: 0.05,
    STAT_STRS['MSPD']: 0.05,
    STAT_STRS['JUMPH']: 1.0,
    STAT_STRS['DODGE']: -0.05,
    STAT_STRS['INVUL']: 0.01,
    STAT_STRS['PRANGE']: 10.0,
    STAT_STRS['DMG']: 0.05,
    STAT_STRS['CRITD']: 0.1,
    STAT_STRS['PROJSPD']: 0.05,
    STAT_STRS['PROJSZ']: 0.1,
    STAT_STRS['PROJNUM']: 0.5
}
PAUSE_MENU_OPTIONS = [
    'Resume',
    'Display Settings',
    'Controls',
    'Return to Title',
    'Quit'
]


# noinspection PyTypeChecker,PyPep8Naming
class SurvGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Survivors")
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT, FONT_SZ)
        self.level_up_menu = None
        self.pause_menu = None
        self.cursor = Cursor()
        self.game_time = MAX_TIME
        self.time_delay = 0

        # Create sprite groups
        self.environment = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.pause_text_sprites = []

        # Add player data from JSON file and create player object
        unitdatafile = open(os.path.join('data', 'unitdata.json'), 'r')
        unitdata = json.loads(str(unitdatafile.read()))
        unitdatafile.close()
        self.P1 = Player(unitdata['Char1'])
        self.players.add(self.P1)
        self.p_exp = 0
        self.p_level = 1
        self.to_next_level = BASE_EXP_REQ

        # Add enemy data from JSON file for spawning enemies
        enemydatafile = open(os.path.join('data', 'enemydata.json'), 'r')
        self.enemydata = json.loads(str(enemydatafile.read()))
        enemydatafile.close()

        # Generate platforms, walls, and doors
        self.floor = Obstacle(vec(WIDTH * 0.5, HEIGHT), 'plat_floor.png')
        self.platforms.add(self.floor)
        self.environment.add(self.floor)
        for i in range(-PLAT_RANGE, PLAT_RANGE):
            plat = Obstacle(vec(WIDTH * (i - 0.5), HEIGHT * 0.65), 'plat_med.png')
            self.environment.add(plat)
            self.platforms.add(plat)
            plat = Obstacle(vec(WIDTH * i, HEIGHT * 0.77), 'plat_med.png')
            self.environment.add(plat)
            self.platforms.add(plat)

        for i in range(-PLAT_RANGE, PLAT_RANGE):
            plat = Obstacle(vec(WIDTH * (i - 0.13), HEIGHT * 0.85), 'wall_med.png')
            self.environment.add(plat)
            self.platforms.add(plat)
            roll = random.randint(0, len(STATS) - 1)
            if 0 <= i < len(self.P1.weapons):
                lock_type = type(self.P1.weapons.sprites()[i]).__name__
                door = WeapDoor(vec(WIDTH * (i + 0.13), HEIGHT * 0.85), 'door.png', lock_type, 2)
            else:
                door = StatDoor(vec(WIDTH * (i + 0.13), HEIGHT * 0.85), 'door.png', STATS[roll], 2)
            self.environment.add(door)
            self.doors.add(door)
            self.platforms.add(door)

        heart = StatPickup(vec(WIDTH * 0.2, HEIGHT * 0.93), STAT_STRS['MAXHP'])
        self.pickups.add(heart)

        pygame.mouse.set_visible(False)

    def spawn_enemies(self):
        for enemy in self.enemydata['Ground']:
            e = GroundEnemy(self.enemydata['Ground'][enemy])
            self.enemies.add(e)
        for enemy in self.enemydata['Flying']:
            e = FlyingEnemy(self.enemydata['Flying'][enemy])
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

    def handle_level_up_screen(self, time_update: int):
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
                        # print(option)
                        self.handle_level_option(option)
            if event.type == KEYDOWN:
                # Choose bonus options using keys 1-6
                if event.key == pygame.K_1:
                    option = self.level_up_menu.get_button_text(0)
                    self.handle_level_option(option)
                elif event.key == pygame.K_2:
                    option = self.level_up_menu.get_button_text(1)
                    self.handle_level_option(option)
                elif event.key == pygame.K_3:
                    option = self.level_up_menu.get_button_text(2)
                    self.handle_level_option(option)
                elif event.key == pygame.K_4:
                    option = self.level_up_menu.get_button_text(3)
                    self.handle_level_option(option)
                elif event.key == pygame.K_5:
                    option = self.level_up_menu.get_button_text(4)
                    self.handle_level_option(option)
                elif event.key == pygame.K_6:
                    option = self.level_up_menu.get_button_text(5)
                    self.handle_level_option(option)

    def handle_level_option(self, option: str):
        if option == '':
            return
        self.P1.gain_stat_bonus(option, LEVEL_BONUSES[option])
        self.level_up_menu.kill()
        self.level_up_menu = None
        self.cursor.kill()

    def add_pause_menu(self):
        self.pause_menu = Menu(PAUSE_MENU_OPTIONS, vec(self.displaysurface.get_rect().center))

        # Add player stats for display
        font = pygame.font.SysFont(FONT, FONT_SZ - 6)
        stats = self.P1.get_stats()
        for s in stats:
            text = font.render(f'{s}: {stats[s]["value"]},     Level: {stats[s]["level"]}', True, TEXTCOLOR)
            text = pygame.transform.scale_by(text, DISP_SCALE)
            self.pause_text_sprites.append(text)

    def handle_pause_screen(self, time_update: int):
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.handle_pause_option('Resume')

    def handle_pause_option(self, option: str):
        if option == '':
            return
        if option == 'Resume':
            self.pause_menu.kill()
            self.pause_menu = None
            self.cursor.kill()
            self.pause_text_sprites = []
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
        time.sleep(1)
        self.displaysurface.fill(END_SCRN_COLOR)
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    def display_text(self):
        # Display timer as MM:SS
        minutes = int(self.game_time / 60)
        seconds = int(self.game_time - minutes * 60)
        if minutes < 10:
            minutes = '0' + str(minutes)
        if seconds < 10:
            seconds = '0' + str(seconds)

        text_time = self.font.render(f'Time: {minutes}:{seconds}', True, TEXTCOLOR)
        text_time = pygame.transform.scale_by(text_time, DISP_SCALE)
        hp = self.P1.get_health()
        mhp = self.P1.get_max_health()
        text_health = self.font.render(f'Health: {hp}/{mhp}', True, TEXTCOLOR)
        text_health = pygame.transform.scale_by(text_health, DISP_SCALE)
        level_pct = round(100 * self.p_exp / self.to_next_level, 2)
        text_level = self.font.render(f'Level: {self.p_level} [{level_pct}%]', True, TEXTCOLOR)
        text_level = pygame.transform.scale_by(text_level, DISP_SCALE)

        self.displaysurface.blit(text_time, (0, 0))
        self.displaysurface.blit(text_health, (0, TEXTBOXHT))
        self.displaysurface.blit(text_level, (0, 2 * TEXTBOXHT))

    def display_menus(self):
        if self.level_up_menu:
            self.displaysurface.blit(self.level_up_menu.image, self.level_up_menu.rect)
            self.level_up_menu.display()
            self.displaysurface.blit(self.cursor.image, self.cursor.rect)
        elif self.pause_menu:
            self.displaysurface.blit(self.pause_menu.image, self.pause_menu.rect)
            self.pause_menu.display()
            height = 3 * TEXTBOXHT
            for entity in self.pause_text_sprites:
                self.displaysurface.blit(entity, (0, height))
                height += TEXTSTATHT
            self.displaysurface.blit(self.cursor.image, self.cursor.rect)

    def display(self):
        # Display objects
        self.displaysurface.fill(BGCOLOR)
        self.environment.draw(self.displaysurface)
        for door in self.doors:
            door.display_lock()
        self.pickups.draw(self.displaysurface)
        self.enemies.draw(self.displaysurface)
        self.players.draw(self.displaysurface)
        self.bullets.draw(self.displaysurface)
        self.display_menus()
        self.display_text()
        pygame.display.update()

    def handle_player_movement(self):
        # Handle horizontal movement and collisions and door lock checks
        self.P1.move_x()
        door_hits = pygame.sprite.spritecollide(self.P1, self.doors, False)
        if door_hits:
            for door in door_hits:
                door.handle_lock_check(self.P1)
        plat_hits = pygame.sprite.spritecollide(self.P1, self.platforms, False)
        if plat_hits:
            for plat in plat_hits:
                self.P1.handle_collision_x(plat)

        # Handle vertical movement and collisions and door lock checks
        self.P1.move_y()
        door_hits = pygame.sprite.spritecollide(self.P1, self.doors, False)
        if door_hits:
            for door in door_hits:
                door.handle_lock_check(self.P1)
        plat_hits = pygame.sprite.spritecollide(self.P1, self.platforms, False)
        if plat_hits:
            for plat in plat_hits:
                self.P1.handle_collision_y(plat)

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.P1.jump()
                if event.key == pygame.K_r:
                    self.P1.dodge()
                if event.key == pygame.K_ESCAPE:
                    self.add_pause_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.P1.cancel_jump()
            if event.type == EVENTS['SPAWNENEMIES']:
                self.spawn_enemies()
            if event.type == EVENTS['GAINEXP']:
                self.p_exp += event.value
                if self.p_exp >= self.to_next_level:
                    self.add_level_up_menu()
            if event.type == EVENTS['GAINSTAT']:
                self.P1.gain_stat_bonus(event.stat, event.value)
            if event.type == EVENTS['PLAYERHEAL']:
                self.P1.heal_percent(event.value)

    def handle_enemy_collisions(self):
        pass

        '''
        enemy_plat_hits = pygame.sprite.groupcollide(self.enemies, self.platforms, False, False)
        for enemy in enemy_plat_hits:
            for plat in enemy_plat_hits[enemy]:
                enemy.handle_collision_x(plat)

        enemy_plat_hits = pygame.sprite.groupcollide(self.enemies, self.platforms, False, False)
        for enemy in enemy_plat_hits:
            for plat in enemy_plat_hits[enemy]:
                enemy.handle_collision_y(plat)
        '''

    def handle_item_pickups(self):
        hits = pygame.sprite.spritecollide(self.P1, self.pickups, False)
        if hits:
            for pickup in hits:
                pickup.collect()

    def handle_player_hits(self):
        hits = pygame.sprite.spritecollide(self.P1, self.enemies, False)
        if hits:
            self.P1.take_hit(hits[0])

    def handle_enemy_hits(self):
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, False)
        for enemy in hits:
            for bullet in hits[enemy]:
                # TODO: Rewrite models
                crit_chance = self.P1.get_crit_chance()
                crit_mod = self.P1.get_crit_mod()
                enemy.take_damage(bullet.get_damage(crit_chance, crit_mod))
                bullet.handle_collision()
                if not enemy.alive():
                    enemy_pos = enemy.get_pos()
                    hp_chance = random.randint(1, 100)
                    if hp_chance <= POT_DROP_RT:
                        size = random.randint(1, 100)
                        if size <= 20:
                            pot = 'HealL'
                        elif size <= 50:
                            pot = 'HealM'
                        else:
                            pot = 'HealS'
                        drop = HealthPickup(enemy_pos, pot)
                    else:
                        loot = LOOT_TABLE[enemy.get_name()]
                        drop = ExpPickup(enemy_pos, loot)
                    self.pickups.add(drop)

    def update_objects(self, time_update: int):
        self.P1.update(time_update)
        ppos = vec(self.P1.get_pos())
        prange = self.P1.get_pickup_range()
        offset = self.P1.get_scroll_dist()
        self.enemies.update(ppos, offset)
        self.pickups.update(ppos, prange, offset)
        self.platforms.update(offset)
        self.floor.recenter(ppos)

    def run(self):
        pygame.time.set_timer(EVENTS['SPAWNENEMIES'], SPAWN_DELAY)

        while True:
            time_update = self.clock.tick(FPS)
            self.game_time = MAX_TIME - int((pygame.time.get_ticks() - self.time_delay) / 1000)
            self.bullets = self.P1.get_bullets()

            # Check loss conditions
            if not self.P1.alive():
                return
            if self.game_time == 0:
                return

            if self.pause_menu:                                 # Pause menu open
                self.handle_pause_screen(time_update)
            else:
                if self.level_up_menu:                          # Level up menu open
                    self.handle_level_up_screen(time_update)
                else:                                           # Game is active
                    self.handle_player_movement()
                    self.update_objects(time_update)    # Update objects and scroll screen
                    self.handle_enemy_collisions()      # Handle enemies colliding with walls and platforms
                    self.handle_item_pickups()          # Handle player grabbing pickups
                    self.handle_player_hits()           # Handle player taking hits
                    self.handle_enemy_hits()            # Handle player shooting enemies
                    self.handle_game_events()           # Handle events (timers, keyboard events, etc.)

            self.display()


if __name__ == '__main__':
    mygame = SurvGame()
    mygame.run()
    mygame.end_game()
