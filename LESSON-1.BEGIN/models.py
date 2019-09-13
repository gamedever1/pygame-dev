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
