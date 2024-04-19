import pygame

# Values related to screen height and width
BASE_HEIGHT = 480
BASE_WIDTH = 854
HEIGHT = 1080
WIDTH = 1920
DISP_SCALE = HEIGHT / BASE_HEIGHT

FPS = 60
FRIC = -0.15
ACC = 0.5 * DISP_SCALE
FONT = 'Arial'

# Stats
STAT_STRS = {
    'MAXHP': 'Max HP',
    'CRITC': 'Crit Chance',
    'ASPD': 'Attack Speed',
    'MSPD': 'Move Speed',
    'JUMPH': 'Jump Height',
    'DODGE': 'Dodge Cooldown',
    'INVUL': 'Invulnerability',
    'PRANGE': 'Pickup Range',
    'DMG': 'Damage',
    'CRITD': 'Crit Damage',
    'PROJSPD': 'Projectile Speed',
    'PROJSZ': 'Weapon Size',
    'PROJNUM': 'Projectile Count'
}

# Custom Events
EVENTS = {
    'SPAWNENEMIES': pygame.USEREVENT,
    'GAINEXP': pygame.USEREVENT + 1,
    'GAINSTAT': pygame.USEREVENT + 2,
    'PLAYERHEAL': pygame.USEREVENT + 3
}
