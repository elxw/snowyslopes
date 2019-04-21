import pygame
import platforms
import math
from locals import *
import load
from camera2 import Camera
from entity import Entity
from physics import *
import random
from pygame import *
import pygame


def makeIce(platforms): # prevents generating new ice coords each time
    iceCoords = {}
    for i in range(len(platforms)):
        p = platforms[i]
        iceLength = random.randint(64, 250)
        if i == 0:
            start = random.randint(400, 700)
        else: start = random.randint(64, 774)
        iceCoords[p] = p.outlineList[start:start+iceLength]
    return iceCoords

class Ice(Entity):
     def __init__(self, x, y, platform, iceCoords):
        super().__init__()
        list = iceCoords[platform]

        newSurface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        newSurface.fill(Color(100, 100, 100))
        newSurface.set_colorkey((100, 100, 100))
        pygame.draw.lines(newSurface, (66, 134, 244), False, list, 4)
        newSurface.set_alpha(80)

        self.image = newSurface
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)



