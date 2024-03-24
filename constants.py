import math
import os

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
MENU_BUTTON_WIDTH = 135

# Stats
MAXHP = 'Max HP'
CRITC = 'Crit Chance'
ASPD = 'Attack Speed'
MSPD = 'Move Speed'
JUMPH = 'Jump Height'
DODGE = 'Dodge Cooldown'
INVUL = 'Invulnerability'
DMG = 'Damage'
CRITD = 'Crit Damage'
PROJSPD = 'Projectile Speed'
PROJSZ = 'Weapon Size'
PROJNUM = 'Projectile Count'

STATS = [
    MAXHP,
    CRITC,
    ASPD,
    MSPD,
    JUMPH,
    DODGE,
    INVUL,
    DMG,
    CRITD,
    PROJSPD,
    PROJSZ,
    PROJNUM
]
LEVEL_BONUSES = {
    MAXHP: 10,
    CRITC: 0.05,
    ASPD: 0.05,
    MSPD: 0.05,
    JUMPH: 1,
    DODGE: -0.05,
    INVUL: 0.01,
    DMG: 0.05,
    CRITD: 0.1,
    PROJSPD: 0.05,
    PROJSZ: 0.05,
    PROJNUM: 0.1
}

LOCK_PATH = 'images\\environment\\locks'
LOCK_IMG_PATHS = {
    'Base': os.path.join(LOCK_PATH, 'lock_base.png'),
    'FireShooter': os.path.join(LOCK_PATH, 'fire.png'),
    'LitShooter': os.path.join(LOCK_PATH, 'lit.png'),
    'IceShooter': os.path.join(LOCK_PATH, 'ice.png'),
    MAXHP: os.path.join(LOCK_PATH, 'maxhp.png'),
    CRITC: os.path.join(LOCK_PATH, 'critc.png'),
    ASPD: os.path.join(LOCK_PATH, 'aspd.png'),
    MSPD: os.path.join(LOCK_PATH, 'mspd.png'),
    JUMPH: os.path.join(LOCK_PATH, 'jumph.png'),
    DODGE: os.path.join(LOCK_PATH, 'dodge.png'),
    INVUL: os.path.join(LOCK_PATH, 'invul.png'),
    DMG: os.path.join(LOCK_PATH, 'dmg.png'),
    CRITD: os.path.join(LOCK_PATH, 'critd.png'),
    PROJSPD: os.path.join(LOCK_PATH, 'projspd.png'),
    PROJSZ: os.path.join(LOCK_PATH, 'projsz.png'),
    PROJNUM: os.path.join(LOCK_PATH, 'projnum.png')
}
# for stat in STATS:
#     LOCK_IMG_PATHS[stat] = os.path.join(LOCK_PATH, 'maxhp.png')
LOCK_NUM_PATHS = {
    0: os.path.join(LOCK_PATH, 'lock_0.png'),
    1: os.path.join(LOCK_PATH, 'lock_1.png'),
    2: os.path.join(LOCK_PATH, 'lock_2.png')
}


'''
    3: os.path.join(LOCK_PATH, 'lock_3.png'),
    4: os.path.join(LOCK_PATH, 'lock_4.png'),
    5: os.path.join(LOCK_PATH, 'lock_5.png'),
    6: os.path.join(LOCK_PATH, 'lock_6.png'),
    7: os.path.join(LOCK_PATH, 'lock_7.png'),
    8: os.path.join(LOCK_PATH, 'lock_8.png'),
    9: os.path.join(LOCK_PATH, 'lock_9.png')
'''