import sys
import time
import pygame
from pygame.locals import *
from actor import Player, Enemy
from platform import Platform
from constants import WIDTH, HEIGHT, FPS, MAX_TIME

vec = pygame.math.Vector2


# noinspection PyTypeChecker
class SurvGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Survivors")
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        # self.camera_offset = 0

        self.floor = Platform(vec(WIDTH / 2, HEIGHT))
        self.P1 = Player()
        self.enemy1 = Enemy()
        self.enemy2 = Enemy()
        self.enemy3 = Enemy()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.floor)
        self.all_sprites.add(self.enemy1)
        self.all_sprites.add(self.enemy2)
        self.all_sprites.add(self.enemy3)
        self.all_sprites.add(self.P1)

        self.actors = pygame.sprite.Group()
        self.actors.add(self.P1)
        self.actors.add(self.enemy1)
        self.actors.add(self.enemy2)
        self.actors.add(self.enemy3)

        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.enemy1)
        self.enemies.add(self.enemy2)
        self.enemies.add(self.enemy3)

        self.platforms = pygame.sprite.Group()
        self.platforms.add(self.floor)

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
        invul = False
        invul_timer = 0
        camera_pos = vec(0, HEIGHT - 100)

        while True:
            if self.P1.get_health() <= 0:
                return
            for enemy in self.enemies:
                if enemy.get_health() <= 0:
                    enemy.kill()

            bullets = self.P1.get_bullets()

            # Invincibility wears off after 2 seconds
            # Turn player invincibility off and reset invulnerability tracking
            if invul_timer > 2000:
                print(f'Timer: {invul_timer}')
                self.P1.vulnerable()
                invul = False
                invul_timer = 0

            self.P1.move()
            for enemy in self.enemies:
                enemy.move()
            if self.P1.out_of_bounds():
                for enemy in self.enemies:
                    enemy.scroll(self.P1.vel.x + 0.5 * self.P1.acc.x)
                self.floor.scroll(self.P1.vel.x + 0.5 * self.P1.acc.x)
            # camera_pos = self.P1.move_player(camera_pos)
            # self.floor.move(self.P1.rect.centerx)

            # self.camera_offset = WIDTH // 2 - self.P1.acc.x - self.P1.rect.width // 2

            # Handle player landing
            plat_hits = pygame.sprite.spritecollide(self.P1, self.platforms, False)
            if plat_hits:
                self.P1.land(plat_hits[0].rect.top)

            # Handle damage from enemies
            enemy_hits = pygame.sprite.spritecollide(self.P1, self.enemies, False)
            if enemy_hits:
                invul = not self.P1.take_damage(enemy_hits[0].get_damage())

            # Handle player shooting enemies
            for bullet in bullets:
                proj_hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
                for enemy in proj_hits:
                    enemy.take_damage(5)

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

            # Set enemy direction
            for enemy in self.enemies:
                enemy.set_facing(enemy.pos_greater_x(self.P1))

            # Display timer as MM:SS
            minutes = int(game_time / 60)
            seconds = int(game_time - minutes * 60)
            if minutes < 10:
                minutes = '0' + str(minutes)
            if seconds < 10:
                seconds = '0' + str(seconds)
            text_time = self.font.render(f'Time: {minutes}:{seconds}', False, (0, 0, 0))

            text_health = self.font.render(f'Health: {self.P1.get_health()}', False, (0, 0, 0))

            for entity in self.all_sprites:
                self.displaysurface.blit(entity.surf, entity.rect)
            for bullet in bullets:
                self.displaysurface.blit(bullet.surf, entity.rect)
            self.displaysurface.blit(text_time, (0, 0))
            self.displaysurface.blit(text_health, (0, 30))

            pygame.display.update()
            time_update = self.clock.tick(FPS)
            self.P1.update(time_update)
            if invul:
                invul_timer += time_update


if __name__ == '__main__':
    mygame = SurvGame()
    mygame.run()
    mygame.end_game()
