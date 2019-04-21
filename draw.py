import pygame
from pygame import *
from locals import *
import load, random
from tree import Tree

class Draw(object):
    NEW = 0
    LOAD = 1
    BACK = 2

    TEXTCOLOR = (155, 192, 219)
    def __init__(self, screen):
        self.mouse = pygame.mouse
        self.timer = pygame.time.Clock()
        self.screen = screen
        self.bgColor = (208, 229, 246)
        self.canvas =pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), SRCALPHA, 32)
        self.screen.set_colorkey(self.bgColor)
        self.points = []
        self.filename = None
        self.numDrawings = 0
        self.slopeColor = (236, 247, 255)
        self.selection = 0
        self.font = load.load_font("Nexa Light", 40)
        self.drawingMode = False
        self.selectionMode = True
        self.loadMode = False
        self.findingImages = True
        self.terrains = []
        self.platforms = []
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
        self.resetScreen()
        while not self.done:
            self.screen.fill(self.bgColor)

            if self.selectionMode:
                title = load.load_image("drawing mode")
                self.screen.blit(title, (0, 20))
                self.makeButtons("NEW DRAWING", Draw.NEW)
                self.makeButtons("LOAD DRAWINGS", Draw.LOAD)
                self.makeButtons("BACK", Draw.BACK)
                for tree in self.trees:
                    self.screen.blit(tree.image, tree.rect)

            if self.drawingMode:
                font = load.load_font("Nexa Bold", 20)
                self.screen.blit(load.load_image("instructions"), (100, 0))
               
                # guide dots
                pygame.draw.circle(self.screen, (159, 194, 252), 
                                   (3, SCREEN_HEIGHT*2//5+20), 5)
                # the screen_height*2//5 is used in platform also so change
                pygame.draw.circle(self.screen, (159, 194, 252), 
                                  (SCREEN_WIDTH-3, SCREEN_HEIGHT*2//5+20), 5)

                pygame.draw.circle(self.screen, (236, 247, 255), 
                                   (self.mouse.get_pos()), 5)
                if self.renderLine:
                    self.render()

                self.canvas.convert_alpha()
                self.screen.convert_alpha()
                self.screen.blit(self.canvas, (0, 0))
                if self.numDrawings >= 1:
                    color = Draw.TEXTCOLOR
                else: color = (250, 250, 255)
                self.screen.blit(font.render(str(self.numDrawings) + 
          " drawings saved", True, color), (SCREEN_WIDTH-200, SCREEN_HEIGHT-30))

            if self.loadMode:
                if self.findingImages:
                    for drawing in range(1, 10):
                        try:
                            name = "terrain" + str(drawing * 100)
                            img = pygame.transform.scale(
                                        load.load_image(str(name)), (200, 119))
                            self.terrains.append(img)
                        except:
                            # no more platform images
                            self.findingImages = False

                for i in range(len(self.terrains)):
                    x = 240 + (245 * (i%3))
                    y = 200 * (i//3)
                    width = 200
                    height = 119
                    rect = Rect(x-200, y, width, height)
                    self.screen.blit(self.terrains[i], rect)

                help = self.font.render("Click to select platforms", 
                                        True, Draw.TEXTCOLOR)
                help2 = self.font.render("Press P to play", True, 
                                         Draw.TEXTCOLOR)
                self.screen.blit(help, (175, SCREEN_HEIGHT-150))
                self.screen.blit(help2, (250, SCREEN_HEIGHT-100))
               
                    
            pygame.display.update()
            left_pressed, middle_pressed, right_pressed = mouse.get_pressed()

            self.timer.tick(60)
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if self.selectionMode:
                    if e.type == KEYDOWN:
                        if e.key == K_UP:
                            self.selection -= 1
                            if self.selection < 0:
                                self.selection = 0
                        if e.key == K_DOWN:
                            self.selection += 1
                            if self.selection > Draw.BACK:
                                self.selection = Draw.BACK
                            if self.selection < 0:
                                self.selction = 0
                        if e.key == K_RETURN:
                            self.selectionMode = False
                            if self.selection == 0:
                                self.drawingMode = True
                            elif self.selection == 1:
                                self.loadMode = True
                            else: 
                                self.done = True


                if self.drawingMode:
                    if left_pressed:
                        pygame.draw.circle(self.canvas, self.slopeColor, 
                                           pygame.mouse.get_pos(), 2)
                        self.points.append((pygame.mouse.get_pos()[0], 
                                            pygame.mouse.get_pos()[1]-5))
                                       
                    elif e.type == KEYDOWN and e.key == K_r:
                        self.renderLine = not self.renderLine
                    elif e.type == KEYDOWN and e.key == K_p:
                        self.done = True
                    elif e.type == KEYDOWN and (e.key == K_s):
                        if self.points != [] and self.renderLine: 
                            # can't save empty drawing or dots
                            self.filename = ("terrain%s.png" %
                                             (str((self.numDrawings+1)*100)))
                            pygame.image.save(self.canvas, self.filename)
                            self.numDrawings += 1 
                            # num drawings only increases after a save
                            print("file %s has been saved" % str(self.filename))
                    elif e.type == KEYDOWN and e.key == K_n:
                        self.resetScreen()

                if self.loadMode:
                    # this feature is mostly for demo purposes
                    if left_pressed:
                        if 20 < pygame.mouse.get_pos()[1] < 120:
                            if 40 < pygame.mouse.get_pos()[0] < 220:
                                if "1" not in self.platforms:
                                    self.platforms.append("1")
                            elif 240 < pygame.mouse.get_pos()[0] < 460:
                                if "2" not in self.platforms:
                                    self.platforms.append("2")
                            elif pygame.mouse.get_pos()[0] > 520:
                                if "3" not in self.platforms:
                                    self.platforms.append("3")
                        if 220 < pygame.mouse.get_pos()[1] < 320:
                            if 40 < pygame.mouse.get_pos()[0] < 220:
                                if "4" not in self.platforms:
                                    self.platforms.append("4")
                            elif 240 < pygame.mouse.get_pos()[0] < 460:
                                if "5" not in self.platforms:
                                    self.platforms.append("5")
                            elif pygame.mouse.get_pos()[0] > 520:
                                if "6" not in self.platforms:
                                    self.platforms.append("6")
                    elif e.type == KEYDOWN and e.key == K_p:
                        if self.platforms != []:
                            self.done = True

                    for num in self.platforms:
                        if int(num) > len(self.terrains):
                            self.platforms.remove(num)
        if self.drawingMode:
            return self.numDrawings
        elif self.loadMode:
            return self.platforms
        else:
            return None
                    
    def render(self):
        newSurface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        newSurface.fill(Color(100, 100, 100))
        newSurface.set_colorkey((100, 100, 100))
        self.points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.points.append((-1, SCREEN_HEIGHT))
        self.points.append((-1, SCREEN_HEIGHT*2//5+20))
        pygame.draw.polygon(newSurface, (236, 247, 255), self.points, 0)
        self.canvas.blit(newSurface, (0,0))

    def resetScreen(self):
        self.renderLine = False
        self.points = []
        self.canvas =pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), SRCALPHA, 32)
        self.screen.blit(self.canvas, (0, 0))
        pygame.display.update()

    def makeButtons(self, text, num):
        textColor = (255, 255, 255)
        if self.selection == num:
            textColor = (50, 150, 225)
        image = self.font.render(text, True, textColor)
        rect = image.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.top = 330 + num * rect.height * 1.4 + 20

        self.screen.blit(image, rect)



