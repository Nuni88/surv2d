import os
import json
import pygame
from constants import FPS, STAT_STRS, DISP_SCALE, EVENTS

vec = pygame.math.Vector2

pickupdatafile = open(os.path.join('../data', 'pickupdata.json'), 'r')
PICKUPDATA = json.loads(str(pickupdatafile.read()))
pickupdatafile.close()
BASE_IMG_PATH = '../images/pickups'


class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, data):
        super().__init__()
        image = pygame.image.load(os.path.join(BASE_IMG_PATH, data['image']))
        self.image = pygame.transform.scale_by(image, DISP_SCALE)
        self.pos = vec(pos)
        self.rect = self.image.get_rect(center=pos)
        self.value = data['value']

    def update(self, ppos, range, offset):
        self.pos.x -= offset
        self.rect.center = self.pos

    def collect(self):
        pass

    def scale_to_screen(self, scale):
        self.image = pygame.transform.scale_by(self.image, scale)


class ExpPickup(Pickup):
    def __init__(self, pos, ptype):
        super().__init__(pos, PICKUPDATA['EXP'][ptype])
        self.vel = vec(0, 0)

    def update(self, ppos, range, offset):
        self.pos.x -= offset
        if self.pos.distance_to(ppos) <= range * DISP_SCALE:
            dx, dy = (ppos.x - self.pos.x, ppos.y - self.pos.y)
            self.vel = vec(dx / FPS, dy / FPS)
            self.pos += self.vel
        self.rect.center = self.pos

    def collect(self):
        e = pygame.event.Event(EVENTS['GAINEXP'], {'value': self.value})
        pygame.event.post(e)
        self.kill()


class HealthPickup(Pickup):
    def __init__(self, pos, ptype):
        super().__init__(pos, PICKUPDATA['HEAL'][ptype])

    def collect(self):
        e = pygame.event.Event(EVENTS['PLAYERHEAL'], {'value': self.value})
        pygame.event.post(e)
        self.kill()


class StatPickup(Pickup):
    def __init__(self, pos, ptype):
        super().__init__(pos, PICKUPDATA['STATS'][ptype])
        self.stat = ptype

    def collect(self):
        e = pygame.event.Event(EVENTS['GAINSTAT'], {'stat': self.stat, 'value': self.value})
        pygame.event.post(e)
        self.kill()
