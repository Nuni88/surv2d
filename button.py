import pygame
import os
from constants import HEIGHT, FONT, DISP_SCALE

# Modifiable values
TEXTCOLOR = (0, 0, 0)   # (R, G, B)
BUTTON_FONT_SIZE = HEIGHT // 40
TEXT_OFFSET_X = 0.22
TEXT_OFFSET_Y = 0.24


class Button(pygame.sprite.Sprite):
    def __init__(self, text, center):
        super().__init__()
        
        self.text = text
        self.surf = pygame.transform.scale_by(pygame.image.load(os.path.join('images', 'button.png')), DISP_SCALE)
        self.rect = self.surf.get_rect(center=center)
        
    def show_text(self):
        pygame.font.init()
        game_font = pygame.font.SysFont(FONT, BUTTON_FONT_SIZE)
        
        text_render = game_font.render(self.text, False, TEXTCOLOR)
        self.surf.blit(text_render, (self.rect.width * TEXT_OFFSET_X, self.rect.height * TEXT_OFFSET_Y))

    def scale_to_screen(self, scale):
        self.surf = pygame.transform.scale_by(self.surf, scale)
