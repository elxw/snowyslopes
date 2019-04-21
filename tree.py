import pygame

from pygame import *
from locals import *

import random, load

from entity import Entity


def init():
    Tree.images = []
    Tree.images.append(load.load_image("tree1"))
    Tree.images.append(load.load_image("tree2"))
    Tree.images.append(load.load_image("tree3"))


def makeTrees(platforms):
    treeDict = {}
    for i in range(len(platforms)):
        p = platforms[i]
        numTrees = random.randint(1, 6) # trees per platform
        for tree in range(numTrees):
            x = random.randint(10, 945) # tree left
            y0 = p.outlineList[x][1] + 10 
            y1 = p.outlineList[x+75][1] + 10
            if p not in treeDict:
                treeDict[p] = [] # list of tuples
            treeDict[p].append((x,max(y0, y1)))
    return treeDict


class Tree(Entity):
    images = None
    def __init__(self, x, y, type=None):
        super().__init__()
        if not Tree.images:
            tree.init()
        self.x = x
        self.y = y
        if type != None:
            self.treeType = type
        else: 
            self.treeType  = int(random.choice("111223"))
        image = Tree.images[self.treeType-1]
        self.image = pygame.transform.scale(image, (75, 150))
        self.rect = Rect(self.x, (self.y - self.image.get_height()), 
                         self.image.get_width(), self.image.get_height())

        