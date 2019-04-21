import pygame
from pygame import *
import load
import random

from tree import Tree
from rain import Rain
from snow import Snow

from locals import *


class Menu(object):
    # Home Screen
    NEWGAME = 0
    HELP = 1
    QUIT = 2

    # Game Selection Screen
    GAME = 0
    DRAW = 1
    BACK = 2

    def __init__(self, screen, gameSelection=False):
        self.screen = screen
        self.gameSelection = gameSelection
        self.font = load.load_font("Nexa Light", 40)
        self.timer = pygame.time.Clock()
        self.selection = 0
        self.bg = Surface((32, 32))
        self.titleImg = load.load_image("title")
        self.offset = 175
        self.mouse = pygame.mouse

        s = random.choice("01")
        self.snowing = int(s)
        if not self.snowing:
            r = random.choice("00000001")
            self.raining = int(r)
        else:
            self.raining = False
        self.rain = Rain()
        self.snow = Snow()

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
            self.bg.convert()
            if not self.raining:
                self.bg.fill(Color(208, 229, 246))
            else:
                self.bg.fill((135, 156, 183))

            for y in range(32):
                for x in range(32):
                    self.screen.blit(self.bg, (x * 32, y * 32))

            for tree in self.trees:
                self.screen.blit(tree.image, tree.rect)

            if self.raining:
                self.rain.update()
                self.rain.draw(self.screen)

            if self.snowing:
                self.snow.update()
                self.snow.draw(self.screen)

            if not self.gameSelection:
                self.render("PLAY", Menu.NEWGAME)
                self.render("HELP", Menu.HELP)
                self.render("QUIT", Menu.QUIT)
            else:
                self.render("BEGIN GAME", Menu.GAME)
                self.render("DRAWING MODE", Menu.DRAW)
                self.render("BACK", Menu.BACK)

            rect = self.titleImg.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.centery = self.offset
            self.screen.blit(self.titleImg, rect)

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
                        if not self.gameSelection:
                            if self.selection > Menu.QUIT:
                                self.selection = Menu.QUIT
                        else:
                            if self.selection > Menu.BACK:
                                self.selection = Menu.BACK
                            if self.selection < 0:
                                self.selction = 0
                    if e.key == K_RETURN:
                        self.done = True
        return self.selection

    def render(self, text, num):
        # draws buttons
        textColor = (255, 255, 255)
        if self.selection == num:
            textColor = (50, 150, 225)
        image = self.font.render(text, True, textColor)
        rect = image.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.top = self.titleImg.get_height() + num * rect.height * 1.4 + 20

        self.screen.blit(image, rect)
