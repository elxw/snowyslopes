# randomization adapted from https://www.dropbox.com/s/yogmtrpgd10ywec/particle.zip

import pygame

from pygame import *
from locals import *

import random, load, math

from entity import Entity
from camera2 import Camera, complex_camera


def init():
    Particle.imgs = []
    Particle.imgs.append(load.load_image("glow1"))
    Particle.imgs.append(load.load_image("glow2"))
    Particle.imgs.append(load.load_image("glow4"))
    Particle.imgs.append(load.load_image("squareglow"))

    if Particle.particleList == []: 
        Particle.makeParticles()

def update(x, y, angle, speed):
    for particle in Particle.particleList:
        particle.update(x, y, angle, speed)

def draw(screen, camera):
    for particle in Particle.particle_sprites:
        screen.blit(particle.image, camera.apply(particle))

class Particle(Entity):  
    imgs = None
    particleList = []
    particle_sprites = pygame.sprite.Group()
    numParticles = 50

    def __init__(self, size, velocity, direction, spread):
        super().__init__()
        if not Particle.imgs:
            particles.init()
        self.velocity = velocity
        self.direction = direction
        self.spread = spread
        self.size = size
        self.addition = 0
        self.image = pygame.transform.scale(Particle.imgs[random.randint(0, 3)],
                    (int(self.size), int(self.size)))
        self.rect = Rect(0, 0, self.image.get_width(), self.image.get_height())

    @staticmethod
    def makeParticles():
        for particle in range(Particle.numParticles):
            velocity = random.randint(1, 10)
            direction = (-1,0)
            spread = (random.randint(1, 5), random.randint(1,5))
            size = 5
            particle = Particle(size, velocity, direction, spread)
            Particle.particleList.append(particle)
            Particle.particle_sprites.add(particle)

    def update(self, x, y, angle, speed):
        self.rect.right += (self.velocity + self.addition * 
                            self.spread[0]/4)*self.direction[0]
        self.rect.top += (self.velocity + self.addition * 
                          self.spread[1]/4)*self.direction[1]

        if self.size > 0: 
            if 18 < speed < 25:
                self.size -= -0.214*speed + 6.21 
                #(22, 1.5), (15, 3) function for length of scarf
            elif speed > 25:
                self.size -= 1.5
            else:
                self.size -= 4.5

            self.velocity += 0.75
            if self.addition < 20: 
                self.addition += 1
        else:
            # resets 
            self.direction = (-1, random.sample([-1, 1], 1)[0]*math.sin(angle))
            self.addition = 0
            self.spread = (random.randint(1, 10), random.randint(1,10))
            self.size = random.randint(3, 10) 
            self.velocity = random.randint(1, 5)

            if speed > 18:
                imgNum = random.choice("0123")
            else:
                imgNum = random.choice("03")
            speedFactor = 0.7 if speed < 18 else 1 # size when speed > 18
            if imgNum == "1": # big glow
                self.image = pygame.transform.scale(Particle.imgs[int(imgNum)],
                                                (int(self.size*1.2*speedFactor),
                                                int(self.size*1.2*speedFactor)))
            elif imgNum == "3": # small square
                resize = random.randint(3, 4)
                self.image = pygame.transform.scale(Particle.imgs[int(imgNum)], 
                                            (int(self.size*speedFactor//resize), 
                                            int(self.size*speedFactor//resize)))
            else:
                self.image = pygame.transform.scale(Particle.imgs[int(imgNum)],
                     (int(self.size*speedFactor), int(self.size*speedFactor)))
            self.rect.right = x
            self.rect.top = y - 5
 

