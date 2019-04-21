import math

def pixelPerfectCollision(player, platform):
        # adapted from http://pygame.org/wiki/FastPixelPerfect
        rect1 = player.rect
        rect2 = platform.rect
        clip = rect1.clip(rect2)

        hm1 = player.hitmask
        hm2 = platform.hitmask

        x1 = clip.x - rect1.x
        y1 = clip.y - rect1.y
        x2 = clip.x - rect2.x
        y2 = clip.y - rect2.y

        for y in range(0, clip.height):
            for x in range(clip.width-1, 0, -1): # checks collision from top? left
                 if hm1[x+x1][y+y1] and hm2[x+x2][y+y2]: # neither are blank pixels
                    return (y2+y, x+x2, x+x1, y+y1)
        return None

def distance(x0, y0, x1, y1):
    return (math.sqrt((x0-x1)**2 + (y0-y1)**2))

def getSlope(x0, y0, x1, y1):
    return ((y1-y0) / (x1-x0))

def getAngle(opp, adj): # relative to x-axis
    result = math.atan2(-opp, adj)
    if result < 0: 
        result += 2*math.pi
    return result * (180/math.pi)

def radians(angle):
    return angle*math.pi/180



