import pygame

import load
from entity import Entity 
from locals import *

class Score(Entity):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.updatedScore = 0

        self.font = load.load_font("Nexa Light", 30)
        self.image = self.font.render("SCORE: 0", True, ((236, 247, 255)))

        self.rect = Rect(50, 30, self.image.get_width(),
                         self.image.get_height())
        self.rect.left = 100
        self.rect.top = 5 # revise these numbers

    def update(self):
        if self.updatedScore > self.score:
            self.score = self.updatedScore
            self.image = self.font.render("Score: "
                                     + str(self.score), True, (236, 247, 255))
            self.rect = Rect(50, 30, self.image.get_width(), 
                             self.image.get_height())

    def add(self, points):    
        self.updatedScore += points
        self.update()

    def getScore(self):
        return self.updatedScore