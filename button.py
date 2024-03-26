import pygame
import os
from constants import BUTTON_FONT_SIZE, DISP_SCALE

button_font = 'Arial'


class Button(pygame.sprite.Sprite):
    def __init__(self, text, center):
        super().__init__()
        
        self.text = text
        self.surf = pygame.transform.scale_by(pygame.image.load(os.path.join('images', 'button.png')), DISP_SCALE)
        self.rect = self.surf.get_rect(center=center)
        
    def show_text(self):
        pygame.font.init()
        game_font = pygame.font.SysFont(button_font, BUTTON_FONT_SIZE)
        
        text_render = game_font.render(self.text, False, (0, 0, 0))
        self.surf.blit(text_render, (self.surf.get_width() / 8, self.surf.get_height() / 4))

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)
