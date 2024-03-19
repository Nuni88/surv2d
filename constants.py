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
MENU_BUTTON_WIDTH = 135

# Stats
MAXHP = 'MaxHP'
CRITC = 'Crit Chance'
ASPD = 'Attack Speed'
MSPD = 'Move Speed'
JUMPH = 'Jump Height'
INVUL = 'Invulnerability'
DMG = 'Damage'
CRITD = 'Crit Damage'
PROJSPD = 'Projectile Speed'
PROJSZ = 'Weapon Size'
PROJNUM = 'Projectile Count'

LEVEL_OPTIONS = [
    MAXHP,
    CRITC,
    ASPD,
    MSPD,
    JUMPH,
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
    INVUL: 0.01,
    DMG: 0.05,
    CRITD: 0.1,
    PROJSPD: 0.05,
    PROJSZ: 0.05,
    PROJNUM: 0.1
}
