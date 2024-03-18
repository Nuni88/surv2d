import math
import enum

HEIGHT = 500
WIDTH = 500
ACC = 0.5
FRIC = -0.12
FPS = 60
MOVE_EDGE_LEFT = WIDTH * 0.1
MOVE_EDGE_RIGHT = WIDTH * 0.9
SHOOTING_DELAY = 1000
GRAVITY = 0.9
MAX_TIME = 300
ACC_ANGLE = math.pi

BUTTON_FONT_SIZE = 12
MENU_TRANSPARENCY = 255
MENU_BUTTON_HEIGHT = 23
MENU_BUTTON_WIDTH = 90

LEVEL_UP_OPTIONS = [
    'MaxHealth',
    'CritChance',
    'AttackSpeed',
    'MoveSpeed',
    'JumpHeight',
    'InvulDuration',
    'Damage',
    'CritDamage',
    'ProjSpeed',
    'WeaponArea',
    'NumProjectiles'
]

LEVEL_UP_BONUSES = {
    'MaxHealth': 10,
    'CritChance': 0.05,
    'AttackSpeed': 0.05,
    'MoveSpeed': 0.05,
    'JumpHeight': 1,
    'InvulDuration': 0.01,
    'Damage': 0.05,
    'CritDamage': 0.1,
    'ProjSpeed': 0.05,
    'WeaponArea': 0.05,
    'NumProjectiles': 0.1
}
