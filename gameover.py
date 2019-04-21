import pygame
from pygame import * 
from locals import *

import os, sys, load, random

from tree import Tree


class GameOver(object):

    REPLAY = 0
    QUIT = 1

    def __init__(self, screen, score=0):
        self.screen = screen
        self.font = load.load_font("Nexa Light", 40)
        self.titleFont = load.load_font("Nexa Bold", 50)
        self.score = score
        message = "YOUR SCORE WAS " + str(int(self.score))
        self.gameover = load.load_image("game over")
        self.title = self.titleFont.render(message, True, (255, 255, 255))
        self.done = False
        self.bg = Surface((32,32))
        self.selection = 0
        self.timer = pygame.time.Clock()
         # random trees
        self.numTrees = random.randint(10, 15)
        self.trees = pygame.sprite.Group()
        increment = SCREEN_WIDTH//self.numTrees
        for t in range(self.numTrees):
            # better random distribution
            x = random.randint(t*increment-5, (t+1)*increment+5) 
            img = int(random.choice("11123"))
            y = SCREEN_HEIGHT + random.randint(10, 60)
            tree = Tree(x, y, img)
            self.trees.add(tree)

    def run(self):
        while not self.done:
            self.bg.convert()
            self.bg.fill(Color(208, 229, 246))

            for y in range(32): # background
                for x in range(32):
                    self.screen.blit(self.bg, (x * 32, y * 32))

            for tree in self.trees:
                self.screen.blit(tree.image, tree.rect)

            rect = self.gameover.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = 50
            self.screen.blit(self.gameover, rect)

            rect = self.title.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = self.gameover.get_height()+ 25 + rect.height * 1.5
            self.screen.blit(self.title, rect)

            self.render("REPLAY", GameOver.REPLAY)
            self.render("QUIT", GameOver.QUIT)

            pygame.display.flip()

            self.timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    self.done = True
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN:
                    if e.key == K_UP:
                        self.selection -= 1
                        if self.selection < 0:
                            self.selection = 0
                    if e.key == K_DOWN:
                        self.selection += 1
                        if self.selection > GameOver.QUIT:
                            self.selection = GameOver.QUIT
                    if e.key == K_RETURN:
                        self.done = True
        return self.selection


    def render(self, text, selection):
        textColor = (255,255,255)
        if self.selection == selection:
            textColor = (50, 150, 225)

        image = self.font.render(text, True, textColor)
        rect = image.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.top = self.gameover.get_height()+200+selection * rect.height * 1.4

        self.screen.blit(image, rect)







