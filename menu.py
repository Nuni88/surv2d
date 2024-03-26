import pygame
from button import Button
from constants import HEIGHT, WIDTH

vec = pygame.math.Vector2

MENU_TRANSPARENCY = 255
MENU_BUTTON_HEIGHT = HEIGHT // 21
MENU_BUTTON_WIDTH = WIDTH // 6


class Menu(pygame.sprite.Sprite):
    def __init__(self, options, center):
        super().__init__()
        height = len(options) * (MENU_BUTTON_HEIGHT + 1)
        surface = vec(MENU_BUTTON_WIDTH, height)
        center = vec(self.adjust_pos(center.x, center.y, surface.x, surface.y))
        
        self.surf = pygame.Surface(surface)
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(MENU_TRANSPARENCY)
        self.rect = self.surf.get_rect(center=center)
        
        self.options = []
        height = 0
        diff = MENU_BUTTON_HEIGHT / 2
        for option in options:
            self.options.append(Button(option, vec(self.rect.centerx, self.rect.top + height + diff)))
            height += MENU_BUTTON_HEIGHT
        
    def display(self):
        height = 0
        for option in self.options:
            self.surf.blit(option.surf, (0, height))
            option.show_text()
            height += MENU_BUTTON_HEIGHT + 1

    # TODO: Modify loop
    def get_option(self, cursor) -> str:
        for option in self.options:
            hit = pygame.sprite.collide_rect(cursor, option)
            if hit:
                return option.text
        return ''

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)

    @staticmethod
    def adjust_pos(x, y, width, height) -> (int, int):
        if x + width / 2 > WIDTH:
            x = WIDTH - width / 2
        elif x - width / 2 < 0:
            x = width / 2
        if y + height / 2 > HEIGHT:
            y = HEIGHT - height / 2
        elif y - height / 2 < 0:
            y = height / 2

        return x, y
