import pygame
from button import Button
from constants import HEIGHT, WIDTH

vec = pygame.math.Vector2

# Modifiable values
MENU_TRANSPARENCY = 255
BUTTON_HEIGHT = HEIGHT // 21
BUTTON_WIDTH = WIDTH // 6
BGCOLOR = pygame.Color('black')


class Menu(pygame.sprite.Sprite):
    def __init__(self, options, center):
        super().__init__()
        height = len(options) * BUTTON_HEIGHT
        # height = len(options) * (BUTTON_HEIGHT + 1)
        surface = vec(BUTTON_WIDTH, height)
        center = vec(self.adjust_pos(center.x, center.y, surface.x, surface.y))
        
        self.image = pygame.Surface(surface)
        self.image.fill(BGCOLOR)
        self.image.set_alpha(MENU_TRANSPARENCY)
        self.rect = self.image.get_rect(center=center)
        
        self.options = []
        height = 0
        diff = BUTTON_HEIGHT / 2
        for option in options:
            self.options.append(Button(option, vec(self.rect.centerx, self.rect.top + height + diff)))
            height += BUTTON_HEIGHT
        
    def display(self):
        height = 0
        for option in self.options:
            self.image.blit(option.image, (0, height))
            option.show_text()
            height += BUTTON_HEIGHT

    # TODO: Modify loop
    def get_option(self, cursor) -> str:
        for option in self.options:
            hit = pygame.sprite.collide_rect(cursor, option)
            if hit:
                return option.text
        return ''

    def get_button_text(self, button_num) -> str:
        return self.options[button_num].text

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)

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
