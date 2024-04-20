import os
import json
import copy
import pytest
import pygame
from models.actor import Actor
from models.errorhandler import *

vec = pygame.math.Vector2
testfile = open(os.path.join('data', 'unitdata.json'), 'r')
testdata = json.loads(str(testfile.read()))
testfile.close()


@pytest.fixture
def new_actor():
    """Return a new Actor object."""
    return Actor(pygame.image.load(testdata['Char1']['frame_left']))


def test_create(new_actor):
    pygame.init()
    assert isinstance(new_actor, Actor), type_error(Actor, type(new_actor))
    assert isinstance(new_actor.image, pygame.surface.Surface), type_error(pygame.surface.Surface, type(new_actor.image))
    assert new_actor.rect == new_actor.image.get_rect(), val_not_equal_error(new_actor.image.get_rect(), new_actor.rect)
    assert new_actor.vel == vec(0, 0), val_not_equal_error(vec(0, 0), new_actor.vel)
    assert new_actor.acc == vec(0, 0), val_not_equal_error(vec(0, 0), new_actor.acc)
    assert new_actor.pos == vec(0, 0), val_not_equal_error(vec(0, 0), new_actor.pos)
    assert new_actor.health == 0, val_not_equal_error(0, new_actor.health)


def test_compare_pos():
    a1 = Actor(pygame.image.load(testdata['Char1']['frame_left']))
    a2 = Actor(pygame.image.load(testdata['Char1']['frame_left']))
    assert a1.pos_greater_x(a2) is False
    a1.pos.x += 1
    assert a1.pos_greater_x(a2) is True
    a2.pos.x += 1
    assert a1.pos_greater_x(a2) is False


def test_move(new_actor):
    new_actor.move()
    assert new_actor.rect.midbottom == new_actor.pos, val_not_equal_error(new_actor.pos, new_actor.rect.midbottom)


def test_get_health(new_actor):
    assert isinstance(new_actor.get_health(), int), type_error(int, type(new_actor.get_health()))
    assert new_actor.get_health() == new_actor.health, value_error(new_actor.health, new_actor.get_health())


def test_get_pos(new_actor):
    assert isinstance(new_actor.get_pos(), tuple), type_error(tuple, type(new_actor.get_pos()))
    assert new_actor.get_pos() == new_actor.rect.center, value_error(new_actor.rect.center, new_actor.get_pos())


def test_scale(new_actor):
    w, h = new_actor.image.get_width(), new_actor.image.get_height()
    new_actor.scale_to_screen(5.0)
    assert w * 5 == new_actor.image.get_width(), value_error(new_actor.image.get_width(), w * 5)
    assert h * 5 == new_actor.image.get_height(), value_error(new_actor.image.get_height(), h * 5)
