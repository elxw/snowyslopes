import pygame

# shortcut to load fonts and images, converted to alpha

def load_font(name, size):
    try:
        return pygame.font.Font("assets/" + name + ".ttf", size)
    except:
        return pygame.font.Font("assets/" + name + ".otf", size)

def load_image(name):
    try:
        return pygame.image.load("assets/" + name + ".png").convert_alpha()
    except:
        return pygame.image.load(name + ".png").convert_alpha() 