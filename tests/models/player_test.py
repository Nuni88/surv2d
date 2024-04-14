import os
import json
import pytest
import pygame
from models.player import Player
from models.obstacle import Obstacle
from models.door import Door
from models.errorhandler import *

vec = pygame.math.Vector2

testfile = open(os.path.join('data', 'unitdata.json'), 'r')
testdata = json.loads(str(testfile.read()))
testfile.close()

@pytest.fixture
def new_player():
    """Return a new Player object."""
    return Player(testdata['Char1'])

@pytest.fixture
def new_obs(new_player):
    """Return a new Obstacle object."""
    return Obstacle(vec(new_player.pos), 'plat_floor.png')

def test_pygame_not_init(new_player):
    pass

def test_create(new_player):
    pygame.init()
    assert isinstance(new_player, Player), type_error(Player)
    assert isinstance(new_player.image, pygame.surface.Surface), type_error(pygame.surface.Surface)
    s1, s2 = new_player.stats, testdata['Char1']['stats']
    assert s1 == s2, val_not_equal_error(s2, s1)
    m1, m2 = new_player.mods, testdata['Char1']['mods']
    assert m1 == m2, val_not_equal_error(m2, m1)

def test_create_null_data():
    with pytest.raises(ValueError):
        p = Player(None)

def test_create_bad_type():
    with pytest.raises(TypeError):
        p = Player('a')

def test_update(new_player):
    pass

def test_update_bad_type(new_player):
    with pytest.raises(TypeError):
        new_player.update('a')

def test_update_out_of_bounds(new_player):
    with pytest.raises(ValueError):
        new_player.update(-1)

def test_move_x(new_player):
    new_player.move_x()
    assert new_player.rect.midbottom == new_player.pos, val_not_equal_error(new_player.pos, new_player.rect.midbottom)

def test_move_y(new_player):
    new_player.move_y()
    assert new_player.rect.midbottom == new_player.pos, val_not_equal_error(new_player.pos, new_player.rect.midbottom)

# TODO: Add to test
def test_handle_collision_x(new_player, new_obs):
    new_player.handle_collision_x(new_obs)
    assert new_player.vel.x == 0, val_not_equal_error(0, new_player.vel.x)
    assert new_player.rect.midbottom == new_player.pos, val_not_equal_error(new_player.pos, new_player.rect.midbottom)

def test_handle_collision_x_bad_type(new_player):
    with pytest.raises(TypeError):
        new_player.handle_collision_x(Player())

def test_handle_collision_x_bad_value(new_player):
    with pytest.raises(ValueError):
        new_player.handle_collision_x(None)

# TODO: Add to test
def test_handle_collision_y(new_player, new_obs):
    new_player.handle_collision_y(new_obs)
    assert new_player.vel.y == 0, val_not_equal_error(0, new_player.vel.y)
    assert new_player.rect.midbottom == new_player.pos, val_not_equal_error(new_player.pos, new_player.rect.midbottom)

def test_handle_collision_y_bad_type(new_player):
    with pytest.raises(TypeError):
        new_player.handle_collision_y(Player())

def test_handle_collision_y_bad_value(new_player):
    with pytest.raises(ValueError):
        new_player.handle_collision_y(None)

def test_jump(new_player):
    new_player.jump()
    assert new_player.jumping == True, val_bool_error(True)

@pytest.mark.parametrize('healpct', [
    0.1,
    0.2,
    0.35,
    0.76,
    0.91
])
def test_heal_percent(new_player, healpct):
    new_player.health = 0
    new_player.heal_percent(healpct)
    assert isinstance(new_player.health, int), type_error(int)
    h = new_player.health
    m = int(healpct * new_player.stats['Max HP']['value'])
    assert h == m, val_not_equal_error(m, h)

@pytest.mark.parametrize('healpct', [
    0.1,
    0.2,
    0.35,
    0.76,
    0.91
])
def test_heal_percent_overheal(new_player, healpct):
    new_player.health = int(new_player.stats['Max HP']['value'] * 0.9)
    new_player.heal_percent(healpct)
    assert isinstance(new_player.health, int), type_error(int)
    h = new_player.health
    m = new_player.stats['Max HP']['value']
    assert h == m, val_not_equal_error(m, h)

@pytest.mark.parametrize('healpct', [
    0.0,
    -1.0,
    -0.5
])
def test_heal_percent_bad_value(new_player, healpct):
    with pytest.raises(ValueError):
        new_player.heal_percent(healpct)

@pytest.mark.parametrize('healpct', [
    'a',
    [1,2,3],
    {'a':1}
])
def test_heal_percent_bad_type(new_player, healpct):
    with pytest.raises(TypeError):
        new_player.heal_percent(healpct)

@pytest.mark.parametrize('stat, level', [
    ('Max HP', 1),
    ('Attack Speed', 1),
    ('Invulnerability', 1)
])
def test_has_req_stat(new_player, stat, level):
    r = new_player.has_req_stat(stat, level)
    assert isinstance(r, bool), type_error(bool)
    assert r == True, val_bool_error(True)

@pytest.mark.parametrize('stat, level', [
    ('Max HP', 5),
    ('Attack Speed', 3),
    ('Invulnerability', 2)
])
def test_has_req_stat_not(new_player, stat, level):
    r = new_player.has_req_stat(stat, level)
    assert isinstance(r, bool), type_error(bool)
    assert r == False, val_bool_error(False)

def test_has_req_stat_bad_stat(new_player):
    with pytest.raises(ValueError):
        new_player.has_req_stat('a', 1)

def test_has_req_stat_bad_lvl(new_player):
    with pytest.raises(ValueError):
        new_player.has_req_stat('Max HP', -1)

def test_get_max_health(new_player):
    assert isinstance(new_player.get_max_health(), int), type_error(int)

def test_get_crit_chance(new_player):
    assert isinstance(new_player.get_crit_chance(), float), type_error(float)

def test_get_crit_mod(new_player):
    assert isinstance(new_player.get_crit_mod(), float), type_error(float)

def test_get_pickup_range(new_player):
    assert isinstance(new_player.get_pickup_range(), float), type_error(float)

def test_get_stats(new_player):
    assert isinstance(new_player.get_stats(), dict), type_error(dict)
