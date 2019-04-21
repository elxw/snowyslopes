# code adapted from
# http://archives.seul.org/pygame/users/Oct-2006/msg00213.html

import pygame

from pygame import *
from locals import *

from math import sin, cos, pi
import random
import load

from entity import Entity


class Rain(Entity):
    raindrops = []

    def __init__(self):
        super().__init__()

    def draw(self, screen):
        for drop in self.raindrops:
            drop.Render(screen)

    def update(self):
        for drop in self.raindrops:
            if drop.remove:
                self.raindrops.remove(drop)
        self.raindrops.append(Rain.Drop(150, random.randint(3, 6),
                                        (255, 255, 255, 255)))

    class Drop(Entity):
        coords = None
        remove = 0

        def __init__(self, height, speed, color):
            super().__init__()
            width = 3
            height = int((random.randint(20, 50) * height) / 100)
            self.image = pygame.Surface((width, height),
                                        pygame.SRCALPHA, 32).convert_alpha()
            self.height = self.image.get_height()
            self.yMax = 600 + height
            self.speed = 5
            self.coords = [random.random() * SCREEN_WIDTH, -self.height]
            factor = float(color[3]) / height
            r, g, b = color[:3]
            for i in range(height):
                # opacity depends on location in the drop, for gradient effect
                self.image.fill((r, g, b, int(factor * i)),
                               (1 * cos(pi / 3), i * sin(pi / 3), width - 2, 1))
            self.rect = pygame.Rect(self.coords[0], self.coords[1],
                                self.image.get_width(), self.image.get_height())

        def Render(self, screen):
            self.coords[1] += self.speed
            self.rect.topleft = self.coords
            self.speed += 0.5
            if self.coords[1] > self.yMax:
                self.remove = True
            else:
                screen.blit(self.image, self.coords)
