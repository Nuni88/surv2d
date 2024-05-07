import sys
import pygame
from pygame.locals import *
from models.scene import Scene
from models.menu import Menu
from globals.constants import FPS

vec = pygame.math.Vector2

MENU_OPTIONS = [
    'Start',
    'Display Settings',
    'Controls',
    'Quit'
]
BGCOLOR = pygame.Color('steelblue1')


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        self.menu = Menu(MENU_OPTIONS, vec(self.displaysurface.get_rect().center))
        self.selected_stage = None
        pygame.mouse.set_visible(False)

    def display(self):
        self.displaysurface.fill(BGCOLOR)
        self.displaysurface.blit(self.menu.image, self.menu.rect)
        self.menu.display()
        self.displaysurface.blit(self.cursor.image, self.cursor.rect)
        pygame.display.update()

    def display_controls(self):
        pass

    def display_settings(self):
        pass

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # Left click
                if event.button == 1:
                    menu_hit = pygame.sprite.collide_rect(self.cursor, self.menu)
                    if menu_hit:
                        option = self.menu.get_option(self.cursor)
                        self.handle_menu_option(option)

    def handle_menu_option(self, option: str):
        if option == '':
            return
        if option == 'Start':
            self.selected_stage = 1
            return
        if option == 'Display Settings':
            self.display_settings()
            return
        if option == 'Controls':
            self.display_controls()
            return
        if option == 'Quit':
            pygame.quit()
            sys.exit()

    def run(self) -> int:
        while True:
            self.clock.tick(FPS)
            self.cursor.move()
            self.handle_game_events()
            self.display()

            if self.selected_stage:
                return self.selected_stage
