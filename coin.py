import pygame

from pygame import *
from locals import *
from physics import *

import random, load

from entity import Entity

def init():
    Coin.image = load.load_image("coin")

def makeCoins(platforms):
    coinDict = {}
    for i in range(1, len(platforms)):
        p = platforms[i]
        numCoins = random.randint(3, 10)
        x = random.randint(0, 850)
        y = p.outlineList[x][1] + 280
        coinDict[p] = [(x, y)]
        offset = 0
        for coin in range(numCoins -1):
            newX = x + offset
            newY = p.outlineList[newX][1] + 280
            coinDict[p].append((newX, newY))
            offset += 20
        coinDict[platforms[0]] = None
    return coinDict

def update(coin):
    reduceOpacity = pygame.Surface((coin.image.get_width(), coin.image.get_height()),
                          flags=pygame.SRCALPHA)
    reduceOpacity.fill((0, 0, 0, 10))
    coin.image.blit(reduceOpacity, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    coin.rect.top -= 10

class Coin(Entity):
    image = None

    def __init__(self, x, y):
        super().__init__()
        if not Coin.image:
            coin.init()
        self.x = x
        self.y = y
        image = Coin.image
        self.image = pygame.transform.scale(image, (15, 15))
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(self.x, self.y, self.width, self.height)

