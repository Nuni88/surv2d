import sys
import time
import random
import os
import json
import pygame
from pygame.locals import *
from actor import Player, EnemyOne, EnemyTwo, EnemyThree
from platform import Platform
from pickup import ExpSmall, ExpMed, ExpLarge, MaxHealthPickup, HealthPickup
from constants import WIDTH, HEIGHT, FPS, MAX_TIME

vec = pygame.math.Vector2

LOOT_TABLE = {
    'EnemyOne': ExpSmall,
    'EnemyTwo': ExpMed,
    'EnemyThree': ExpLarge
}


# noinspection PyTypeChecker
class SurvGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Survivors")
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.spawn_delay = 2000

        # Add units from JSON file
        unitdatafile = open(os.path.join('data', 'unitdata.json'), 'r')
        unitdata = json.loads(str(unitdatafile.read()))
        unitdatafile.close()

        self.P1 = Player(unitdata['Char1'])

        self.all_sprites = pygame.sprite.Group()
        self.actors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()

        self.floor = Platform(vec(WIDTH / 2, HEIGHT), 'plat_floor.png')
        self.platforms.add(self.floor)
        self.all_sprites.add(self.floor)
        for i in range(-20, 20):
            plat = Platform(vec(WIDTH * i, HEIGHT * 0.70), 'plat_med.png')
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            plat = Platform(vec(WIDTH * i - WIDTH / 2, HEIGHT * 0.50), 'plat_med.png')
            self.all_sprites.add(plat)
            self.platforms.add(plat)

        heart = MaxHealthPickup(vec(WIDTH / 2, HEIGHT * 0.50 - 20))
        self.all_sprites.add(heart)
        self.pickups.add(heart)

        self.all_sprites.add(self.P1)
        self.actors.add(self.P1)

    def spawn_enemy(self, enemy_type):
        enemy = enemy_type()
        self.all_sprites.add(enemy)
        self.actors.add(enemy)
        self.enemies.add(enemy)

    def end_game(self):
        for entity in self.all_sprites:
            entity.kill()
        time.sleep(1)
        self.displaysurface.fill((255, 0, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    def run(self):
        spawn_timer = 0

        while True:
            if self.P1.get_health() <= 0:
                return

            bullets = self.P1.get_bullets()

            self.P1.move()
            mod = self.P1.get_scroll_dist()
            self.floor.scroll(-mod)
            for enemy in self.enemies:
                enemy.move_to(self.P1)

            # Scroll the screen
            if self.P1.out_of_bounds():
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
                    pickup.collect(self.P1)
                    pickup.kill()

            # Handle player landing
            plat_hits = pygame.sprite.spritecollide(self.P1, self.platforms, False)
            if plat_hits:
                self.P1.land(plat_hits[0])
                # self.P1.land(plat_hits[0].rect.top)

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
                        if hp_chance <= 10:
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
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.P1.shoot()
                '''
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.P1.cancel_jump()

            self.displaysurface.fill((200, 200, 200))

            # Check if time is over
            game_time = MAX_TIME - int(pygame.time.get_ticks() / 1000)
            if game_time == 0:
                return

            # Display timer as MM:SS
            minutes = int(game_time / 60)
            seconds = int(game_time - minutes * 60)
            if minutes < 10:
                minutes = '0' + str(minutes)
            if seconds < 10:
                seconds = '0' + str(seconds)

            text_time = self.font.render(f'Time: {minutes}:{seconds}', False, (0, 0, 0))
            text_health = self.font.render(f'Health: {self.P1.get_health()}/{self.P1.get_max_health()}', False, (0, 0, 0))
            text_level = self.font.render(f'Level: {self.P1.get_level()} [{self.P1.get_exp()}%]', False, (0, 0, 0))

            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for bullet in bullets:
                self.displaysurface.blit(bullet.surf, bullet.rect)
            self.displaysurface.blit(text_time, (0, 0))
            self.displaysurface.blit(text_health, (0, 30))
            self.displaysurface.blit(text_level, (0, 60))

            pygame.display.update()
            time_update = self.clock.tick(FPS)
            self.P1.update_timers(time_update)
            spawn_timer += time_update
            if spawn_timer >= self.spawn_delay:
                self.spawn_enemy(EnemyOne)
                self.spawn_enemy(EnemyTwo)
                self.spawn_enemy(EnemyThree)
                spawn_timer -= self.spawn_delay


if __name__ == '__main__':
    mygame = SurvGame()
    mygame.run()
    mygame.end_game()
