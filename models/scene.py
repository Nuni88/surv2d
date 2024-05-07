import pygame
from pygame.locals import *
from models.cursor import Cursor
from globals.constants import WIDTH, HEIGHT


class Scene:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Survivors")
        self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.cursor = Cursor()
        self.clock = pygame.time.Clock()
