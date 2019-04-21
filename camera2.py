# adapted from http://stackoverflow.com/questions/23175361/how-would-i-make-a-scrolling-camera-in-pygame


import pygame
from locals import *
from pygame import *
from pygame.locals import *

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply2(self, rect):
        return rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stops at left edge
    l = max(-(camera.width-SCREEN_WIDTH), l) # stops at right edge
    t = max(-(camera.height-SCREEN_HEIGHT), t) # stops at bottom
    t = min(0, t)                           # stops at top
    return Rect(l, t, w, h)