import pygame

from pygame import *
from locals import *
from platforms import *
from physics import *

import load
import random
import math

from camera2 import Camera, complex_camera
from player import Player
from entity import Entity
from menu import Menu
from ice import Ice, makeIce
from rock import Rock, Penguin, makeRock
from score import Score
from rain import Rain
from snow import Snow
from tree import Tree, makeTrees
from birds import Bird, generateBirds
from coin import Coin, makeCoins

import coin
import birds
import clouds
import player
import particles
import sys


class Game(object):
    bgColor = [208, 229, 246]
    textColor = (236, 247, 255)

    def __init__(self, screen, timer, custom=False):
        self.screen = screen
        self.timer = timer

        '''Game Mode'''
        if custom != False:  # 0, if no platforms are drawn
            self.custom = True
            if isinstance(custom, list):
                self.customPlatTypes = custom
                self.customNumPlatforms = None
            else:
                self.customNumPlatforms = custom
                self.customPlatTypes = None
        else:
            self.custom = False

        '''Game Mechanics'''
        self.totalGameTime = 1000
        self.gameover = False
        self.gameover_image = None
        self.gameover_rect = None
        self.pause = False
        self.done = False
        font = load.load_font("OpenSans-Semibold", 40)
        self.pause_image = font.render("Paused", True, (236, 247, 255))
        self.pause_rect = self.pause_image.get_rect()
        self.pause_rect.center = self.screen.get_rect().center
        self.exit = True
        self.showFPS = False
        self.noCrashes = False

        '''Background'''
        self.bg = Surface((32, 32))
        self.bgTime = 0
        self.bgColor = Game.bgColor
        self.sundownTime = 0
        self.rainStart = random.randint(0, self.totalGameTime)
        self.rainEnd = self.rainStart + random.randint(150, 500)
        self.rainEndColor = None
        self.darkenTime = (self.rainEnd - self.rainStart) / 3
        self.lightenTime = 2 * (self.rainEnd - self.rainStart) / 3
        self.raining = self.darkening = self.lightening = False
        self.snowing = False
        self.snow = Snow()

        '''Game entities'''
        self.entities = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.ice = pygame.sprite.Group()
        self.player = Player()
        self.entities.add(self.player)
        self.coinCount = 0
        self.flyingBirds = []
        self.collectedCoins = []
        self.clouds = None

        '''Score'''
        self.score = Score()
        self.scoreSprite = pygame.sprite.Group()
        self.scoreSprite.add(self.score)

        '''Platforms'''
        self.platforms = []
        self.numPlatforms = 30
        self.generatePlatforms()
        self.createPlatforms()

        '''Camera'''
        self.totalWidth = 1024 * len(self.platformTypes)
        self.totalHeight = 800
        self.camera = Camera(complex_camera, self.totalWidth, self.totalHeight)

        '''Generating obstacles'''
        self.iceCoords = makeIce(self.platforms)
        rockInfo = makeRock(self.platforms)
        self.treeDict = makeTrees(self.platforms)
        self.birdDict = generateBirds(self.platforms)
        self.coinDict = makeCoins(self.platforms)
        (self.rockRects, self.rockCoords, self.rockAngles) = \
            (rockInfo[0], rockInfo[1], rockInfo[2])

        # ROCKS
        offset = 1024
        for item in range(1, len(self.rockRects)):
            currentPlatform = self.platforms[item]
            x = self.rockRects[currentPlatform][0] + offset
            y = self.rockRects[currentPlatform][1]
            angle = self.rockAngles[currentPlatform]
            obstacle = random.choice("001")
            rock = Rock(x, y, angle) if obstacle == "0" else Penguin(
                x, y, angle)
            self.rocks.add(rock)
            offset += 1024

        # ICE
        iceOffset = 0
        for item in range(self.numPlatforms):
            currentPlatform = self.platforms[item]
            x = iceOffset
            ice = Ice(x, 299, currentPlatform, self.iceCoords)
            self.ice.add(ice)
            iceOffset += 1024

        # TREES
        offset = 0
        for item in range(len(self.treeDict)):
            currentPlatform = self.platforms[item]
            treeCoords = self.treeDict[currentPlatform]
            for tree in treeCoords:
                x = offset + tree[0]
                yOffset = random.randint(5, 20)
                y = tree[1] + 300 + yOffset
                tree = Tree(x, y)
                self.trees.add(tree)
            offset += 1024

        # BIRBS & COINS
        offset = 0
        for item in range(self.numPlatforms):
            currentPlatform = self.platforms[item]
            coords = self.birdDict[currentPlatform]
            coinCoords = self.coinDict[currentPlatform]
            if coords != None:
                for point in coords:
                    x = offset + point[0]
                    y = point[1]
                    bird = Bird(x, y, 0)
                    self.birds.add(bird)
            if coinCoords != None:
                for coin in coinCoords:
                    x = offset + coin[0]
                    y = coin[1]
                    coin = Coin(x, y)
                    self.coins.add(coin)
            offset += 1024

    def run(self):
        while not self.done:
            if not self.pause:
                # update all game entities
                self.camera.update(self.player)
                self.groundSpeed = \
                    self.player.update(
                        self.platforms, self.iceCoords, self.rocks)
                clouds.update(self.bgTime, self.totalGameTime, self.raining)

                for bird in self.birds:
                    if pixelPerfectCollision(self.player, bird) != None:
                        birds.update(bird)
                        self.flyingBirds.append(bird)

                if self.flyingBirds != []:  # bird animation
                    for bird in self.flyingBirds:
                        if bird.rect.top >= 0:
                            birds.update(bird)
                        else:
                            self.flyingBirds.remove(bird)
                            self.birds.remove(bird)

                for c in self.coins:
                    if pixelPerfectCollision(self.player, c) != None:
                        self.bgTime -= 1
                        coin.update(c)
                        self.collectedCoins.append([c, 0])

                if self.collectedCoins != []:  # coin animation
                    existCoins = False
                    for i in range(len(self.collectedCoins)):
                        c, num = self.collectedCoins[i]
                        if c != None and num != None:
                            existCoins = True
                            if num <= 20:
                                coin.update(c)
                                num += 1
                                self.collectedCoins[i] = [c, num]
                            else:
                                self.collectedCoins[i] = [None, None]
                                self.coins.remove(c)
                    if not existCoins:
                        self.collectedCoins = []  # no coins to update

                if self.raining:
                    self.rain.update()
                if self.snowing:
                    self.snow.update()

                particles.update(self.player.rect.centerx,
                                 self.player.rect.centery, self.player.angle,
                                 self.groundSpeed)
                if self.player.crashed and not self.noCrashes:
                    self.exit = False
                    self.setGameOver("You crashed! Press ENTER to exit.")
                elif self.player.crashed and self.noCrashes:
                    self.player.crashed = False
                elif self.player.tooSteep and self.custom:
                    self.exit = False
                    self.setGameOver(
                        "The slopes are too steep! Press ENTER to exit.")
                self.score.add(self.player.getScore())
            self.draw()
            self.handleEvents()
        return self.score.getScore()

    def draw(self):
        self.bg.convert()
        if not self.pause:
            self.bgTime += 1
        if self.bgTime + 1 == self.totalGameTime:
            print(self.player.rect.right // 1024)
            self.exit = False
            self.bgTime += 1  # avoid an endless loop
            self.setGameOver("Time's Up! Press ENTER to exit.")

        if self.bgTime % 5 == 0:
            if self.darkening or self.lightening or self.raining:
                self.bgColor = self.rainSky()
            else:
                self.bgColor = self.getTimeColor()

        color = (self.bgColor[0], self.bgColor[1], self.bgColor[2])
        try:
            self.bg.fill(color)
        except:
            self.bg.fill((59, 82, 119))

        # blit the background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        # draw the sun based on "time of day"
        sun = pygame.transform.scale(load.load_image("sun"), (150, 150))
        if 50 + (SCREEN_HEIGHT) * (self.bgTime / self.totalGameTime) <= 400:
            self.screen.blit(sun, (SCREEN_WIDTH - 150 - 50 *
                            (self.bgTime / self.totalGameTime),
                     50 + (SCREEN_HEIGHT) * (self.bgTime / self.totalGameTime)))

        if abs((50 + (SCREEN_HEIGHT) * (self.bgTime / self.totalGameTime))
                - 250) <= 2:
            self.sundownTime = self.bgTime

        # draw game entities
        for tree in self.trees:
            self.screen.blit(tree.image, self.camera.apply(tree))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
        for ice in self.ice:
            self.screen.blit(ice.image, self.camera.apply(ice))
        for rock in self.rocks:
            self.screen.blit(rock.image, self.camera.apply(rock))
        for bird in self.birds:
            self.screen.blit(bird.image, self.camera.apply(bird))
        for coin in self.coins:
            self.screen.blit(coin.image, self.camera.apply(coin))

        self.scoreSprite.draw(self.screen)
        clouds.draw(self.screen)
        player.drawMessage(self.screen)

        if self.snowing:
            self.snow.draw(self.screen)

        self.checkForRain()

        particles.draw(self.screen, self.camera)

        # Draw game info
        font = load.load_font("Nexa Light", 30)
        fps = font.render("FPS: " + str(int(self.timer.get_fps())),
                          True, Game.textColor)
        speed = font.render("Speed: " + str(int(self.groundSpeed)),
                            True, Game.textColor)
        if self.showFPS:
            self.screen.blit(fps, (50, 60))
        self.screen.blit(speed, (SCREEN_WIDTH - 200, 30))
        timeLeft = "Time Left: "
        timer = font.render(timeLeft, True, Game.textColor)
        rect = timer.get_rect()
        rect.right = int(self.screen.get_rect().centerx)
        rect.top = 30
        self.screen.blit(timer, rect)
        time = font.render(str(self.totalGameTime - self.bgTime),
                           True, Game.textColor)
        rect = time.get_rect()
        rect.left = int(self.screen.get_rect().centerx)
        rect.top = 30
        self.screen.blit(time, rect)

        if self.gameover:
            if self.exit == False:  # when time runs out
                self.pause = True
                self.screen.blit(self.gameover_image, self.gameover_rect)
            else:
                self.done = True

        pygame.display.update()

    def handleEvents(self):
        self.timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.done = True
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if not self.pause:
                    if e.key == K_UP:
                        self.player.moveUp(True)
                    if e.key == K_SPACE:
                        self.player.rotate(True)
                    # cheat: make it rain
                    if e.key == K_r:
                        self.bgTime = self.rainStart
                    # cheat: make it snow
                    if e.key == K_s:
                        self.snowing = not self.snowing
                    # cheat: show FPS
                    if e.key == K_f:
                        self.showFPS = not self.showFPS
                    # cheat: approach end of game
                    if e.key == K_e:
                        self.bgTime = self.totalGameTime - 50
                        self.rainStartColor = 0
                        if self.sundownTime == 0:
                            self.sundownTime = 1
                    # cheat: alter player speeds
                    if e.key == K_z:
                        self.player.groundSpeed += 1
                    elif e.key == K_x:
                        self.player.groundSpeed -= 1
                    # cheat: no crashing!
                    if e.key == K_c:
                        self.noCrashes = not self.noCrashes
                if e.key == K_p:
                    self.pause = not self.pause
                if self.gameover and e.key == K_RETURN:
                    self.exit = True
            elif e.type == KEYUP:
                if e.key == K_UP:
                    self.player.moveUp(False)
                if e.key == K_SPACE:
                    self.player.rotate(False)

    def createPlatforms(self, start=0):
        x = start
        y = 300
        for c in self.platformTypes:
            platformTypes = str(c)
            p = Platform(x, y, platformTypes)
            self.platforms.append(p)
            self.entities.add(p)
            x += p.width

    def generatePlatforms(self):
        self.platformTypes = ["start"]
        for i in range(self.numPlatforms):
            if self.custom:
                if self.customPlatTypes != None:
                    selections = "".join(self.customPlatTypes)
                    r = random.choice(selections)
                    platform = str(int(r) * 100)
                    self.platformTypes.append(platform)

                else: self.platformTypes.append(str(random.randint(1,
                                                self.customNumPlatforms) * 100))
            else:
                # randomly chooses platforms; weighted probability
                self.platformTypes.append(random.choice("911223344556"))
        return self.platformTypes

    def checkForRain(self):
        if abs(self.rainStart - self.bgTime) <= 1:
            # it started raining
            self.rain = Rain()
            self.rainStartColor = self.getTimeColor()
            self.darkening = True

        if self.rainStart < self.bgTime < self.rainEnd:
            # it is raining
            self.raining = True
            self.rain.draw(self.screen)
        else:
            # it's not raining
            self.raining = False

        if abs(self.bgTime - (self.rainStart + self.darkenTime)) <= 1:
            # sky is done darkening
            self.darkening = False

        if abs(self.bgTime - (self.rainStart + self.lightenTime)) <= 1:
            # 2/3 of rain is done, start lightening sky
            self.rainEndColor = self.getTimeColor(
                self.rainEnd + 40)  
            # anticipated color
            self.lightening = True

        if abs(self.bgTime - self.rainEnd - 40) <= 1:
            self.lightening = False

    def getTimeColor(self, time=None):  
        # throwback to rgb color blender
        if time != None:
            bgTime = time
        else:
            bgTime = self.bgTime
        if self.sundownTime != 0:
            # fraction of time elapsed
            r = 208 - ((208 - 59) *
                       ((bgTime - self.sundownTime) / self.totalGameTime))
            g = 229 - ((229 - 82) *
                       ((bgTime - self.sundownTime) / self.totalGameTime))
            b = 246 - ((246 - 119) *
                       ((bgTime - self.sundownTime) / self.totalGameTime))
            if r < 59:
                r = 59
            if g < 82:
                g = 82
            if b < 119:
                b = 119
            return [int(r), int(g), int(b)]
        else:
            return Game.bgColor

    def rainSky(self):
        if self.darkening:
            if self.bgTime <= self.rainStart + self.darkenTime:
                timeElapsed = (self.bgTime - self.rainStart)
                r = (self.rainStartColor[0] - ((self.rainStartColor[0] - 135)
                                               * timeElapsed / self.darkenTime))
                g = (self.rainStartColor[1] - ((self.rainStartColor[1] - 156)
                                               * timeElapsed / self.darkenTime))
                b = (self.rainStartColor[2] - ((self.rainStartColor[2] - 183)
                                               * timeElapsed / self.darkenTime))
                return [int(r), int(g), int(b)]
            else:
                return [135, 156, 183]
        elif self.lightening:
            secondsElapsed = self.bgTime - (self.rainEnd - self.darkenTime)
            if abs(secondsElapsed - (self.rainEnd - self.darkenTime + 40)) <= 5:
                self.raining = self.lightening = self.darkening = False
                # rain effects are over
                return self.rainEndColor
            else:
                a = self.rainEnd - self.darkenTime + 40
                color = self.rainEndColor
                r, g, b = color[0], color[1], color[2]
                newR = int(135 - (135 - r) * (secondsElapsed / a))
                newG = int(156 - (156 - g) * (secondsElapsed / a))
                newB = int(183 - (183 - g) * (secondsElapsed / a))
                return [int(newR), int(newG), int(newB)]
        else:  # just raining
            return [135, 156, 183]

    def setGameOver(self, message="Game Over"):
        # sets game over, shows a message depending on cause of death
        self.gameover = True
        images = []
        font = load.load_font("Nexa Light", 30)
        height = 0
        width = 0
        for text in message.split("\n"):
            images.append(font.render(text, True, (25, 51, 71)))
            height += images[-1].get_height()
            width = images[-1].get_width()
        self.gameover_image = pygame.Surface((width, height), SRCALPHA, 32)
        self.gameover_image.fill((0, 0, 0, 0))
        for i in range(len(images)):
            rect = images[i].get_rect()
            rect.top = i * images[i].get_height()
            rect.centerx = width / 2
            self.gameover_image.blit(images[i], rect)

        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_rect.center = self.screen.get_rect().center
