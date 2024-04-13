import pygame
import os
from models.constants import HEIGHT, FONT, DISP_SCALE

# Modifiable values
TEXTCOLOR = pygame.Color('black')
BUTTON_FONT_SIZE = HEIGHT // 40
TEXT_OFFSET_X = 0.22
TEXT_OFFSET_Y = 0.24


class Button(pygame.sprite.Sprite):
    def __init__(self, text: str, center: pygame.math.Vector2):
        super().__init__()
        
        self.text = text
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join('images', 'button.png')), DISP_SCALE)
        self.rect = self.image.get_rect(center=center)
        
    def show_text(self):
        pygame.font.init()
        game_font = pygame.font.SysFont(FONT, BUTTON_FONT_SIZE)
        
        text_render = game_font.render(self.text, False, TEXTCOLOR)
        self.image.blit(text_render, (self.rect.width * TEXT_OFFSET_X, self.rect.height * TEXT_OFFSET_Y))

    def scale_to_screen(self, scale: float):
        self.image = pygame.transform.scale_by(self.image, scale)
