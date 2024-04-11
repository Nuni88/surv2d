import unittest
import pygame
from models.cursor import Cursor

pygame.init()


class TestCursor(unittest.TestCase):
    def test_create(self):
        cur = Cursor()
        self.assertIsInstance(cur, Cursor)
        self.assertIsInstance(cur.image, pygame.surface.Surface)
        self.assertEqual(cur.rect, cur.image.get_rect())
        
    def test_move(self):
        cur = Cursor()
        cur.move()
        self.assertEqual(cur.rect.topleft, pygame.mouse.get_pos())
        self.assertIsInstance(cur.rect.topleft, tuple)
        
    def test_scale(self):
        cur = Cursor()
        w, h = cur.image.get_width(), cur.image.get_height()
        cur.scale_to_screen(5)
        self.assertEqual(w * 5, cur.image.get_width())
        self.assertEqual(h * 5, cur.image.get_height())


if __name__ == '__main__':
    unittest.main()
