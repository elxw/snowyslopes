import pygame

from pygame import *
from locals import *

from math import sin, cos, pi
import random
import load

from entity import Entity
 
class Snow(Entity):
    snowflakes = []
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        for flake in self.snowflakes:
            flake.Render(screen)

    def update(self):
        for flake in self.snowflakes:
            if flake.remove:
                self.snowflakes.remove(flake)
        direction = (random.random() * random.sample([-1, 1], 1)[0], 3)
        self.snowflakes.append(Snow.Flake(random.randint(2, 5), direction))

    class Flake(Entity):
        coords = None
        remove = 0
 
        def __init__(self, speed, direction):
            super().__init__()
            self.image = pygame.transform.scale(load.load_image("snowflake"), (6, 6))
            self.yMax = SCREEN_HEIGHT
            self.speed = 3
            self.direction = direction
            self.coords = [random.random() * SCREEN_WIDTH, -10]
            self.rect = Rect(self.coords[0], self.coords[1], 
                             self.image.get_width(), self.image.get_height())

        def Render(self, screen):
            self.coords[1] += self.direction[1]
            self.coords[0] += self.direction[0] * random.random()
            self.rect.topleft = self.coords
            self.speed += 0.01
            if self.coords[1] > self.yMax:
                self.remove = True
            else:
                screen.blit(self.image, self.coords)
