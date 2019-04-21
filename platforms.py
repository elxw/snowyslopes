import pygame, load

from pygame import *
from locals import *

from entity import Entity

class Platform(Entity):
    def __init__(self, x, y, type):
        Entity.__init__(self) 
        self.type = type 
        # loads image based on the type of platform
        imgName = "terrain" + str(self.type)
        self.image =pygame.transform.scale(load.load_image(imgName),(1024, 607))
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = Rect(x, y, self.image.get_width(), self.image.get_height())
        self.getPlatformHeight()
        

    def getPlatformHeight(self):
        # returns a list of points outlining the top of the platform
        outlineList = self.mask.outline()
        self.outlineList = []

        rightEdge = []
        leftEdge = []

        for point in outlineList:
            if (point[0] != 0 and point[1] != self.height-1
                and point[0] != self.width-1):
                self.outlineList.append(point)
            if point[0] == 0:
                rightEdge.append(point)
            if point[0] == self.width-1:
                leftEdge.append(point)
               
        self.outlineList.append(min(rightEdge)) if rightEdge != [] \
        else self.outlineList.append((self.width, SCREEN_HEIGHT*2//5+20)) 
        self.outlineList.append(min(leftEdge)) if leftEdge != [] \
        else self.outlineList.append((0, SCREEN_HEIGHT*2//5))
        self.outlineList.sort() 
        self.outlineList.append((self.width, self.outlineList[self.width-1][1]))
