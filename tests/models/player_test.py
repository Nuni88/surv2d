import os
import json
import pytest
import pygame
from models.player import Player

testfile = open(os.path.join('data', 'unitdata.json'), 'r')
testdata = json.loads(str(testfile.read()))
testfile.close()

@pytest.fixture
def new_player():
    """Return a new Player object."""
    return Player(testdata['Char1'])

def test_pygame_not_init(new_player):
    pass

def test_create(new_player):
    pygame.init()
    assert isinstance(new_player, Player)
    assert isinstance(new_player.image, pygame.surface.Surface)
    assert new_player.stats == testdata['Char1']['stats']
    assert new_player.mods == testdata['Char1']['mods']

def test_create_null_data(new_player):
    with pytest.raises(ValueError):
        p = Player(None)

def test_create_bad_type(new_player):
    with pytest.raises(TypeError):
        p = Player('a')

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
    assert isinstance(new_player.health, int)
    assert new_player.health == int(healpct * new_player.stats['Max HP']['value'])

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
    assert isinstance(r, bool)
    assert r == True

@pytest.mark.parametrize('stat, level', [
    ('Max HP', 5),
    ('Attack Speed', 3),
    ('Invulnerability', 2)
])
def test_has_req_stat_not(new_player, stat, level):
    r = new_player.has_req_stat(stat, level)
    assert isinstance(r, bool)
    assert r == False

def test_has_req_stat_bad_stat(new_player):
    with pytest.raises(ValueError):
        new_player.has_req_stat('a', 1)

def test_has_req_stat_bad_lvl(new_player):
    with pytest.raises(ValueError):
        new_player.has_req_stat('Max HP', -1)

def test_get_max_health(new_player):
    assert isinstance(new_player.get_max_health(), int)

def test_get_crit_chance(new_player):
    assert isinstance(new_player.get_crit_chance(), float)

def test_get_crit_mod(new_player):
    assert isinstance(new_player.get_crit_mod(), float)

def test_get_pickup_range(new_player):
    assert isinstance(new_player.get_pickup_range(), float)

def test_get_stats(new_player):
    assert isinstance(new_player.get_stats(), dict)
