# -*- coding: utf-8 -*-
import pygame

class Tile():
    def __init__(self, tileType, movable):
        self.tileType = tileType
        self.isMovable = movable

class Entity(pygame.sprite.Sprite):
    def __init__(self, level):
        self.x, self.y, self.dx, self.dy = 256, 256, 0, 0
        self.level = level
        self.isCasting = False
        self.isMoving = False
        self.isFacingRight = True
        self.offsetX = 8 * 2
        self.offsetY = -32 * 2

        pygame.sprite.Sprite.__init__(self)

    def update(self):
        nextX = (int)((self.x + self.dx) / (16.0 * 16.0 * self.level.gameScale) * 16)
        nextY = (int)((self.y + self.dy) / (16.0 * 16.0 * self.level.gameScale) * 16)
        if (nextX > self.level.xSize - 1 or nextY > self.level.ySize - 1 or nextX < 0 or nextY < 0): return
        if (self.level.getTileAt(nextX, nextY).isMovable):
            self.x += self.dx
            self.y += self.dy

        return ((int)(self.x / (16.0 * 16.0 * self.level.gameScale) * 16), (int)(self.y / (16.0 * 16.0 * self.level.gameScale) * 16))

class Level():
    def __init__(self, xSize, ySize, gameScale):
        self.xSize, self.ySize = xSize, ySize
        self.gameScale = gameScale
        self.tileData = [[] * xSize] * ySize
        self.decorationData = [[] * xSize] * ySize

    def getTileAt(self, xPos, yPos):
        return self.tileData[yPos][xPos]

    def getDecorationAt(self, xPos, yPos):
        return self.decorationData[yPos][xPos]

    def getObjectsAt(self, xPos, yPos):
        return (getTileAt(xPos, yPos), getDecorationAt(xPos, yPos))

    def getAllTiles(self):
        return self.tileData

    def getAllDecorations(self):
        return self.decorationData

    def setTileAt(self, xPos, yPos, data):
        self.tileData[yPos][xPos] = data

    def setDecorationAt(self, xPos, yPos, data):
        self.decorationData[yPos][xPos] = data

    def setAllTiles(self, data):
        self.tileData = data

    def setAllDecorations(self, data):
        self.decorationData = data
        




###################################################################





class gameObj(object):
    def __init__(self, pos, objImage, objName = 'unnamed'):
        self.pos = pos #позиция объекта на карте x,y
        self.img = objImage #картинка объекта

        objImageRect = objImage.get_rect()
        self.img_rect = objImageRect #получение прямоугольной Rect(x=0,y=0,w,h) картинки        
        colorkey = objImage.get_at((0, 0)) #берет цвет самого верхнего левого пикселя
        self.img.set_colorkey(colorkey) #устанавливает этот цвет как цвет прозрачности
        self.img_mask = pygame.mask.from_surface(objImage) # по colorkey-цвету прозрачности создает маску(непрозрачных пикелей)
        self.img_rect.x = pos[0] #устанавливает в прямоугольнике x-координату объекта 
        self.img_rect.y = pos[1] #и y-координату
        
        
        leftmostX = objImageRect.w 
        rightmostX = 0 
        topY = objImageRect.h 
        lowY = 0 
        for imgY in range(objImageRect.h): #расчет прямоугольника, в который вписана картинка объект без прозрачных областей 
            for imgX in range(objImageRect.w):
                if (self.img_mask.get_at((imgX, imgY))) == 1: 
                    if imgY > lowY: 
                        lowY = imgY 

        self.lowestY = lowY # Y-координата самого нижнего непрозрачного пикселя в картинке объекта
