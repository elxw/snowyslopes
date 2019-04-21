import pygame

from pygame import *
from locals import *
from physics import *

import random, load

from entity import Entity

def init():
    Bird.images = []
    Bird.images.append(load.load_image("standing"))
    Bird.images.append(load.load_image("flying1"))
    Bird.images.append(load.load_image("flying2"))

def generateBirds(platforms):
    birdDict = {}
    for i in range(len(platforms)):
        p = platforms[i]
        if int(random.choice("00011")): # 2/5 chance of birds on a platform
            numBirds = random.randint(1, 3)
            x = random.randint(10, 945) # modify based on width after running
            y = p.outlineList[x][1] + 277
            birdDict[p] = [(x, y)]
            offset = 15
            for bird in range(numBirds-1):
                newX = x + offset
                newY  = p.outlineList[newX][1] + 277 + random.randint(0, 5)
                birdDict[p].append((newX,newY))
                offset += random.randint(15, 30)         
        else:
            birdDict[p] = None
    return birdDict

def update(bird):
    img = random.choice("01")
    if img == "1":
        bird.image = pygame.transform.scale(Bird.images[1], (25, 25))
    else:
        bird.image = pygame.transform.scale(Bird.images[2], (25, 25))
    bird.rect.top -= 10
    bird.rect.right += 20

class Bird(Entity):
    images = None

    def __init__(self, x, y, birdType):
        super().__init__()
        if not Bird.images:
            bird.init()

        self.x = x
        self.y = y

        image = Bird.images[birdType]
        self.image = pygame.transform.scale(image, (25, 25))
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(self.x, self.y, self.width, self.height)
