import pygame
import platforms
import math
from locals import *
import load
from camera2 import Camera
from entity import Entity
from physics import *
import random


def init():
    Penguin.image = load.load_image("penguin")
    Rock.image = load.load_image("rock")
    Rock.explosionImages = []
    Rock.explosionImages.append(load.load_image("destructed rock"))
    Rock.explosionImages.append(load.load_image("destructed rock 1"))
    Rock.explosionImages.append(load.load_image("destructed rock 2"))


def makeRock(platforms):
    rectList = {}
    coordList = {}
    angleList = {}
    for i in range(1, len(platforms)):
        p = platforms[i]
        start = random.randint(64, p.width-32)
        x = start
        y = p.outlineList[start][1]+280
        coordList[p] = (x, y) # dictionary of rock coords
        rect = Rect(x, y, 30, 22) # x y width height
        rectList[p] = rect # a dictionary of rects, 1 per platform

        x0, x1 = rect.left%1024, rect.right%1024
        y0, y1 = p.outlineList[x0][1], p.outlineList[x1][1]
        targetAngle = getAngle((y1-y0), rect.width)
        angleList[p] = targetAngle

    return rectList, coordList, angleList

class Rock(Entity):
    image = None
    def __init__(self, x, y, angle):
        super().__init__()
        if not Rock.image:
            rock.init()
        self.image = pygame.transform.rotate(Rock.image, angle)
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(x, y, self.width, self.height)

    def explode(self, num):
        self.image = Rock.explosionImages[num]
        
class Penguin(Entity):
    image = None
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.transform.rotate(Penguin.image, angle)
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(x, y, self.width, self.height)

    def explode(self, num):
        self.image = load.load_image("destructed penguin1")
      





