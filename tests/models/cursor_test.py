import pytest
import pygame
from models.cursor import Cursor


@pytest.fixture
def cursor():
    """Return a new Cursor object."""
    return Cursor()


def test_pygame_not_init(cursor):
    pygame.quit()
    with pytest.raises(RuntimeError):
        cursor.move()


def test_create(cursor):
    pygame.init()
    assert isinstance(cursor, Cursor)
    assert isinstance(cursor.image, pygame.surface.Surface)
    assert cursor.rect == cursor.image.get_rect()


def test_move(cursor):
    cursor.move()
    assert cursor.rect.topleft == pygame.mouse.get_pos()
    assert isinstance(cursor.rect.topleft, tuple)


def test_scale(cursor):
    w, h = cursor.image.get_width(), cursor.image.get_height()
    cursor.scale_to_screen(5.0)
    assert w * 5 == cursor.image.get_width()
    assert h * 5 == cursor.image.get_height()


def test_scale_bad_type(cursor):
    with pytest.raises(TypeError):
        cursor.scale_to_screen('Hello')
