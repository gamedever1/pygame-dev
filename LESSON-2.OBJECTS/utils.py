import pygame
import sys

def loadSpritesheet(filename, xRes, yRes, xScale=1, yScale=1, colorkey=None):
    try:
        file = pygame.image.load(filename).convert()
    except pygame.error as message:
        print('[FATAL] Failed to load spritesheet (' + filename + ')')
        raise(SystemExit, message)

    images = [None] * ((int)(file.get_width() / xRes))
    for i in range(0, len(images)):
        rect = pygame.Rect((i * xRes, 0, xRes, yRes))
        image = pygame.Surface(rect.size).convert()
        image.blit(file, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        images[i] = pygame.transform.scale(image, (xRes * xScale, yRes * yScale))
    return images

def loadCharacterSpritesheet(filename, xRes, yRes, xNum, yNum, xScale=1, yScale=1, colorkey=None):
    try:
        file = pygame.image.load(filename).convert()
    except pygame.error as message:
        print('[FATAL] Failed to load spritesheet (' + filename + ')')
        raise(SystemExit, message)

    output = []
    for i in range(0, yNum):
        images = []
        for x in range(xNum):
            rect = pygame.Rect((xRes * x, yRes * i, xRes, yRes))
            image = pygame.Surface(rect.size).convert()
            image.blit(file, (0, 0), rect)
            if colorkey is not None:
                if colorkey is -1: colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
            image = pygame.transform.scale(image, (xRes * xScale, yRes * yScale))
            images.append((image, image.get_rect()))
        output.append(images)
    return output
