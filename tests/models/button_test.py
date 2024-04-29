import pytest
import pygame
from models.button import Button
from models.errorhandler import *

vec = pygame.math.Vector2


@pytest.fixture
def new_button():
    """Return a new Button object."""
    return Button('Test', vec(0, 0))


def test_create(new_button):
    assert isinstance(new_button, Button), type_error(Button, type(new_button))
    assert isinstance(new_button.image, pygame.surface.Surface), type_error(pygame.surface.Surface, type(new_button.image))
    assert isinstance(new_button.text, str), type_error(str, type(new_button.text))
    r = new_button.image.get_rect(center=vec(0, 0))
    assert new_button.rect == r, val_not_equal_error(r, new_button.rect)


def test_create_bad_type():
    with pytest.raises(TypeError):
        Button(5, vec(0, 0))
        Button('Test', 8)


def test_create_bad_value():
    with pytest.raises(ValueError):
        Button(None, vec(0, 0))
        Button('Test', None)


def test_scale(new_button):
    w, h = new_button.image.get_width(), new_button.image.get_height()
    new_button.scale_to_screen(5.0)
    assert w * 5 == new_button.image.get_width(), val_not_equal_error(new_button.image.get_width(), w * 5)
    assert h * 5 == new_button.image.get_height(), val_not_equal_error(new_button.image.get_height(), h * 5)


def test_scale_bad_type(new_button):
    with pytest.raises(TypeError):
        new_button.scale_to_screen('Hello')
