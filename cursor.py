import pygame
import os
from constants import GRIDLOCS, GRIDSPACESIZE

vec = pygame.math.Vector2


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def move(self):
        pass
        

class SelectionCursor(Cursor):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images', 'select_cursor.png'))
        self.rect = self.surf.get_rect()
        
    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        x = int(mouse_pos[0] / GRIDSPACESIZE)
        y = int(mouse_pos[1] / GRIDSPACESIZE)
        self.rect.topleft = vec(GRIDLOCS[x][y])  # Snap to grid when moving


class MenuCursor(Cursor):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(os.path.join('images', 'menu_cursor.png'))
        self.rect = self.surf.get_rect()

    def move(self):
        self.rect.topleft = pygame.mouse.get_pos()
