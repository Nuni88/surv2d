import pygame
import os
from constants import BUTTON_FONT_SIZE


class Button(pygame.sprite.Sprite):
    def __init__(self, text, center):
        super().__init__()
        
        self.text = text
        self.surf = pygame.image.load(os.path.join('images', 'button.png'))
        self.rect = self.surf.get_rect(center=center)
        
    def show_text(self):
        pygame.font.init()
        game_font = pygame.font.SysFont('Arial', BUTTON_FONT_SIZE)
        
        text_render = game_font.render(self.text, False, (0, 0, 0))
        self.surf.blit(text_render, (self.surf.get_width() / 8, self.surf.get_height() / 4))
