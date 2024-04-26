import pytest
import pygame
from models.cursor import Cursor
from models.errorhandler import *


@pytest.fixture
def new_cursor():
    """Return a new Cursor object."""
    return Cursor()


def test_pygame_not_init(new_cursor):
    pygame.quit()
    with pytest.raises(RuntimeError):
        new_cursor.move()


def test_create(new_cursor):
    pygame.init()
    assert isinstance(new_cursor, Cursor), type_error(Cursor, type(new_cursor))
    assert isinstance(new_cursor.image, pygame.surface.Surface), type_error(pygame.surface.Surface, type(new_cursor.image))
    assert new_cursor.rect == new_cursor.image.get_rect(), val_not_equal_error(new_cursor.image.get_rect(), new_cursor.rect)


def test_move(new_cursor):
    new_cursor.move()
    assert new_cursor.rect.topleft == pygame.mouse.get_pos(), val_not_equal_error(pygame.mouse.get_pos(), new_cursor.rect.topleft)
    assert isinstance(new_cursor.rect.topleft, tuple), type_error(tuple, type(new_cursor.rect.topleft))


def test_scale(new_cursor):
    w, h = new_cursor.image.get_width(), new_cursor.image.get_height()
    new_cursor.scale_to_screen(5.0)
    assert w * 5 == new_cursor.image.get_width(), val_not_equal_error(new_cursor.image.get_width(), w * 5)
    assert h * 5 == new_cursor.image.get_height(), val_not_equal_error(new_cursor.image.get_height(), h * 5)


def test_scale_bad_type(new_cursor):
    with pytest.raises(TypeError):
        new_cursor.scale_to_screen('Hello')
