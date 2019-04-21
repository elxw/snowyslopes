import pygame
from pygame import *
import random
import load
from entity import Entity

from locals import *


def init():
    Cloud.images = []
    Cloud.cloud_sprites = pygame.sprite.Group()
    Cloud.images.append(load.load_image("cloud1"))
    Cloud.images.append(load.load_image("cloud2"))
    Cloud.images.append(load.load_image("cloud3"))
    Cloud.images.append(load.load_image("cloud4"))


def update(timer, totalTime, isRaining):
    if isRaining:
        alpha = 40
    else:
        alpha = int(50 * timer / totalTime)

    if Cloud.time % 50 == 0:
        Cloud.cloudList.append(Cloud(alpha))  # adds a random cloud
        Cloud.cloud_sprites.add(Cloud.cloudList[-1])
    for cloud in Cloud.cloudList:
        cloud.update()
        if cloud.rect.right < 0:
            Cloud.cloudList.remove(cloud)
            Cloud.cloud_sprites.remove(cloud)
    Cloud.time += 1


def draw(screen):
    Cloud.cloud_sprites.draw(screen)


class Cloud(Entity):
    images = None
    cloudList = []
    cloud_sprites = pygame.sprite.Group()
    time = 0

    def __init__(self, alpha=0):
        super().__init__()

        if not Cloud.images:
            clouds.init()

        self.cloudType = random.randint(1, len(Cloud.images))

        image = Cloud.images[self.cloudType - 1]

        x = random.randint(110, 200)  # random sizes
        y = int(x / (5/3))  # keep proportions

        self.image = pygame.transform.scale(image, (x, y))

        # darkenen adapted from 
        # https://gist.github.com/metulburr/a0da897fe38ae631b6cb
        darken = pygame.Surface((self.image.get_width(), self.image.get_height()),
                              flags=pygame.SRCALPHA)
        darken.fill((alpha * 1.3, alpha * 1.3, alpha * 1.3, alpha * 1.1))
        self.image.blit(darken, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        self.rect = pygame.Rect(SCREEN_WIDTH, random.randint(0, 150),
                                self.image.get_width(), self.image.get_height())
        self.dx = -1 * random.randint(3, 5)

    def update(self):
        self.rect.left += self.dx
