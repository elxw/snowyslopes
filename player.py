import pygame
import load

from locals import *
from physics import *

from entity import Entity
from ice import Ice
from rock import Rock
from score import Score
from math import sin, cos, pi


def init():
    Player.image = load.load_image("sledder")


def drawMessage(screen):
    msgNum = 0
    messages = ["SMASHED INTO ROCK!", "JUMPED OVER ROCK!", "SUCCESSFUL TRICK!"]
    font = load.load_font("FuturaT_Bold", 20)
    for i in range(len(Player.msgBools)):
        if Player.msgBools[i]:
            msgNum += 1
            msg = font.render(messages[i], True, (127, 178, 215))
            screen.blit(msg, (SCREEN_WIDTH - 250,
                              SCREEN_HEIGHT - 50 - msgNum * 35))
            # if multiple messages have to be blitted
    msgNum = 0


class Player(Entity):
    image = None
    grav = 1.1
    acc = 0.5
    iceAcc = 0.2
    trickAcc = 1
    msgBools = [False, False, False]  # rockSmash, rockJump, didTrick
    pWidth = 1024
    cameraY = 300

    def __init__(self):
        super().__init__()
        if not Player.image:
            player.init()
        self.image = Player.image
        self.image.convert_alpha()
        self.dx, self.dy = 0, 9
        self.angle = 0
        self.onGround = False
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.doingTrick = self.rotating = False
        self.crashed = self.tooSteep = self.willCrash = False
        self.up = False
        self.falling = True
        self.groundSpeed = 12
        self.message = None
        self.score = 5  # score multiplier
        self.blitCount = 0

    def update(self, platforms, ice=None, rock=None):
        if self.groundSpeed >= 18:  # function for calibrating speed
            dec = 0.013 * self.groundSpeed - .22
            self.groundSpeed -= dec

        if Player.msgBools[0] or Player.msgBools[1] or Player.msgBools[2]:
            self.blitCount += 1
        else:
            self.blitCount = None

        if self.onGround:
            if self.willCrash:
                self.tooSteep = True
            self.falling = False
            if 0 < self.angle % 360 < 90:  # going uphill
                self.groundSpeed -= (Player.acc *
                                     abs(sin(radians(self.angle))))
            else:
                if self.groundSpeed <= 25:
                    self.groundSpeed += (Player.acc *
                                         abs(sin(radians(self.angle))))

            self.dx = self.groundSpeed * cos(radians(self.angle))
            self.dy = self.groundSpeed * -sin(radians(self.angle))

        if self.rotating:
            self.updateAngle(self.angle + 20)

        if not self.onGround:
            self.dy += Player.grav

        self.makeLegalXMove(self.dx,
                        platforms[self.rect.right // Player.pWidth], platforms)
        self.collide(self.dx, 0, platforms)

        if self.up and not self.falling:
            self.dy = (-12)
            self.falling = True

        self.makeLegalYMove(self.dy,
                        platforms[self.rect.right // Player.pWidth], platforms)
        self.collide(0, self.dy, platforms)

        self.icerockCollision(platforms, ice, rock)

        if self.blitCount == 20:
            Player.msgBools[0] = Player.msgBools[
                1] = Player.msgBools[2] = False

        if self.onGround and (240 < self.angle % 360 < 300 
                              or 90 < self.angle % 360 < 180):
            self.tooSteep = True

        return self.groundSpeed

    def makeLegalXMove(self, move, platform, platforms, depth=0):
        # makes a legal move in the x direction depending on player's position
        # relative to the slope
        p = platform
        x = self.rect.left
        x += move  # make the move
        result = self.isLegalX(x, p, platforms)
        if result == True:
            # make the move to the player rect
            self.rect.left += move
        else:
            # offset by how much the player would overlap and make the move
            target1 = result
            self.rect.left, self.rect.top = \
                self.rect.left + move, self.rect.top - target1

    def isLegalX(self, x, p, platforms):
        '''calculates if move is legal; if not, returns how much the player 
        overlaps a legal move is defined as the player's bottom being at the 
        height of the platform'''
        x0 = int(x % Player.pWidth)  # left most point
        x1 = (int((x0 + self.width * (sin(radians(self.angle)))
                   + self.width * (cos(radians(self.angle)))) % Player.pWidth))

        platformY0 = \
            (platforms[self.rect.right // Player.pWidth].outlineList[x0][1])
        # corresponding platform height

        if self.rect.right % Player.pWidth <= Player.pWidth - self.width:
            platformY1 = \
                platforms[self.rect.right // Player.pWidth].outlineList[x1][1]
        else:
            # use next platform
            platformY1 = \
                platforms[self.rect.right //
                          Player.pWidth + 1].outlineList[x1][1]

        bottom0 = (self.rect.top - Player.cameraY
                   + self.width * (sin(radians(self.angle)))
                   + self.width * (cos(radians(self.angle))))
        bottom1 = (self.rect.top - Player.cameraY
                   + self.width * cos(radians(self.angle)))

        if platformY1 >= bottom1 and platformY0 >= bottom0:
            # should always be above slope curve
            return True
        else:
            targetAngle = getAngle((platformY1 - platformY0), self.rect.width)
            if not self.doingTrick:
                self.updateAngle(targetAngle)
            target1 = bottom1 - platformY1
            return target1

    def makeLegalYMove(self, move, platform, platforms, depth=0):
        p = platform
        y = self.rect.top
        y += move  # make the move
        result = self.isLegalY(y, p, platforms)
        if result[0]:
            self.rect.top += move
            return
        else:
            target1 = result[2]
            self.rect.top += math.floor(move - abs(target1))  # correction

    def isLegalY(self, y, p, platforms):
        x0 = self.rect.left % Player.pWidth  # left most point
        x1 = self.rect.right % Player.pWidth  # right most point
        currPlat = self.rect.right // Player.pWidth
        platformY0 = platforms[currPlat].outlineList[x0][1]
        platformY1 = platforms[currPlat].outlineList[x1][1]
        top = y
        bottom0 = (top - Player.cameraY
                   + self.width * (sin(radians(self.angle)))
                   + self.width * (cos(radians(self.angle))))
        bottom1 = (top - Player.cameraY + self.width *
                   cos(radians(self.angle)))

        if platformY1 >= bottom1:  # should always be above slope curve
            return (True, None, None)
        else:
            prevAngle = self.angle % 360
            targetAngle = getAngle(
                (platformY1 - platformY0), self.rect.width) % 360
            if (abs(self.angle - targetAngle) <= 30 or
                abs(self.angle + 360 - targetAngle) <= 30 or
                    abs(self.angle - targetAngle - 360) <= 30):
                pass
            else:
                if not self.doingTrick:
                    print("Too steep", prevAngle, targetAngle)
                    self.willCrash = True
            if not self.doingTrick:
                self.updateAngle(targetAngle)
            target0 = bottom0 - platformY0
            target1 = bottom1 - platformY1
            return (False, target0, target1)

    def updateAngle(self, angle):
        # updates player angle and rotates original image based on the angle
        self.angle = angle
        self.image = pygame.transform.rotate(Player.image, angle)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.hitmask = pygame.surfarray.array_alpha(self.image)

    def isUphill(self, p):
        x0, x1 = self.rect.left % Player.pWidth, \
            self.rect.right % Player.pWidth
        y0, y1 = p.outlineList[x0][1], p.outlineList[x1][1]
        return (y1 < y0)

    def collide(self, dx, dy, platforms):
        p = platforms[self.rect.right // Player.pWidth]
        if pixelPerfectCollision(self, p) != None:
            # collision occurred
            self.onGround = True
            self.dy = 0

            if self.isUphill(p):
                y0, y1 = self.calculateUphill(p)
            else:
                y0, y1 = self.calculateDownhill(p)
            yOverlap = pixelPerfectCollision(self, p)[0]
            xOverlap = pixelPerfectCollision(self, p)[1]
            third = pixelPerfectCollision(self, p)[2]

            targetAngle = getAngle((y1 - y0), self.rect.width)

            if self.doingTrick:
                if self.angle > 360:
                    calcAngle = self.angle % 360
                else:
                    calcAngle = self.angle

                if (abs(targetAngle - calcAngle) <= 25 or
                    abs(targetAngle + 360 - calcAngle) <= 25 or
                        abs(targetAngle - calcAngle - 360) <= 25):
                    # allows for some inaccuracy, takes edge cases into account

                    self.blitCount = 0
                    Player.msgBools[2] = True
                    # successful trick!
                    scoreMultiple = self.angle // 360 + 0.5
                    self.score += int(3 * scoreMultiple)
                    self.groundSpeed += Player.trickAcc  # speed up
                    self.doingTrick = False
                else:  # crashed
                    print("Aiming for", targetAngle, "but", calcAngle)
                    self.crashed = True

            if not self.doingTrick:
                self.updateAngle(targetAngle)
        else:
            self.onGround = False

    def calculateUphill(self, p):
        # returns slope height at player's position going uphill
        x0, x1 = self.rect.left % Player.pWidth, \
            self.rect.right % Player.pWidth
        y0, y1 = p.outlineList[x0][1], p.outlineList[x1][1]
        return (y0, y1)

    def calculateDownhill(self, p):
        # returns slope height at player's position going downhill
        a = self.angle
        x0 = (int(self.rect.right % Player.pWidth
            - (self.width * sin(a * pi / 180)) - self.width) % Player.pWidth)
        x1 = (int(self.rect.right % Player.pWidth
                  - (self.width * sin(a * pi / 180))) % Player.pWidth)
        y0, y1 = p.outlineList[x0][1], p.outlineList[x1][1]
        return (y0, y1)

    def icerockCollision(self, platforms, ice, rock):
        self.currPlat = platforms[self.rect.right // Player.pWidth]
        if (ice[self.currPlat][0][0] <= (self.rect.centerx % Player.pWidth)
                                     <= ice[self.currPlat][-1][0]):
            if not self.falling:
                # speed increases when colliding with ice
                self.groundSpeed += Player.iceAcc
                
        # rock pixel collision
        for r in rock:
            leftRockEdge = r.rect.x
            if pixelPerfectCollision(self, r) != None:
                if self.groundSpeed < 20:  # different from scarf
                    self.crashed = True
                else:  # can smash into rocks at speeds greater than 20
                    self.blitCount = 0
                    Player.msgBools[0] = True
                    n = 0
                    while n < 3:
                        r.explode(n)
                        n += 1
            elif (0 <= self.rect.right % Player.pWidth - leftRockEdge <= 20
                  and self.falling):
                # jumped over rock
                self.blitCount = 0
                Player.msgBools[1] = True

    def getScore(self):
        return self.score

    def moveUp(self, bool):
        if bool:
            self.up = True
        else:
            self.up = False

    def rotate(self, bool):
        if bool and self.falling:
            self.rotating = True
            self.doingTrick = True
        else:
            self.rotating = False
