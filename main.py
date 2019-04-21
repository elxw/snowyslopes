import pygame

from pygame import *
from locals import *
from platforms import *

import load
import math
import random
import player
import rock
import clouds
import particles
import sys
import tree
import birds
import coin

from camera2 import Camera, complex_camera
from player import Player
from entity import Entity
from menu import Menu
from ice import Ice
from game import Game
from draw import Draw
from gameover import GameOver
from menu import Menu
from tree import Tree


def init():
    player.init()
    rock.init()
    clouds.init()
    particles.init()
    tree.init()
    birds.init()
    coin.init()


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Snowy Slopes")
    pygame.display.set_icon(load.load_image("sledderFullsize"))

    init()
    timer = pygame.time.Clock()

    while True:
        timer.tick(60)
        selection = Menu(screen).run()
        if selection == Menu.NEWGAME:
            selection = Menu(screen, gameSelection=True).run()
            if selection == Menu.GAME:
                score = Game(screen, timer).run()
            elif selection == Menu.DRAW:
                numPlatforms = Draw(screen).run()
                if isinstance(numPlatforms, list):
                    platformType = numPlatforms
                    score = Game(screen, timer, custom=platformType).run()
                elif isinstance(numPlatforms, int):
                    score = Game(screen, timer, custom=numPlatforms).run()
                else:
                    main()
            elif selection == Menu.BACK:
                main()
        elif selection == Menu.HELP:
            Help(screen, timer).run()
            score = Game(screen, timer).run()
        elif selection == Menu.QUIT:
            pygame.quit()
            sys.exit()

        # runs after game is over
        newSelection = GameOver(screen, score).run()
        if newSelection == GameOver.QUIT:
            pygame.quit()
            sys.exit()
        elif newSelection == GameOver.REPLAY:
            main()  # resets the game


class Help(object):  # Help Screen info
    def __init__(self, screen, timer):
        self.screen = screen
        self.timer = timer
        self.font = load.load_font("Nexa Light", 20)
        self.bg = Surface((32, 32))
        # random trees
        self.numTrees = random.randint(10, 15)
        self.trees = pygame.sprite.Group()
        increment = SCREEN_WIDTH // self.numTrees
        for t in range(self.numTrees):
            # better random distribution
            x = random.randint(t * increment - 5, (t + 1) * increment + 5)
            img = int(random.choice("111223"))
            y = SCREEN_HEIGHT + random.randint(10, 60)
            tree = Tree(x, y, img)
            self.trees.add(tree)

    def run(self):
        self.done = False
        while not self.done:
            # draw the background
            self.bg.convert()
            self.bg.fill(Color(208, 229, 246))
            for y in range(32):
                for x in range(32):
                    self.screen.blit(self.bg, (x * 32, y * 32))
            # draw the trees
            for tree in self.trees:
                self.screen.blit(tree.image, tree.rect)
            # draw the help screen
            help = (load.load_image("help image"))
            self.screen.blit(help, (0, 0))
            pygame.display.flip()

            self.timer.tick(60)

            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    main()

if __name__ == '__main__':
    main()
