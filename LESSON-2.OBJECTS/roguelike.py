#/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Horizontal collision detection, everything else

import os, pygame
from pygame.locals import *
from random import randint, choice, randrange ###
from utils import loadSpritesheet, loadCharacterSpritesheet
from models import Level, Tile, Entity, gameObj ###



playerType = 'ranger'
gameScale = 2
tileData = [
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        ]
decorationData = [
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        ]

xRes, yRes = (int)(gameScale * 256), (int)(gameScale * 256)
level = Level(16, 16, 2)
level.setAllTiles(tileData)
level.setAllDecorations(decorationData)

def loadTextures():
    global playerTextures, wallTextures, ceilingTextures, floorTextures

    global gameObjectList #глобальная переменная со всеми объектами в игре 
    gameObjectList = []#делаем переменную пустым списком
    
    itemSprites1 = loadSpritesheet('assets/Items1.png', 16, 32, xScale=gameScale, yScale=gameScale) #режем вещи Items1.png на отдельные картинки-объекты
    for i in range(len(itemSprites1)): #для каждой нарезанной картинки-объекта, помещаем его в случайное место на карте
        gameObjectList.append(gameObj([randrange(0, xRes-itemSprites1[i].get_rect().w),randrange(0, yRes - itemSprites1[i].get_rect().h)], itemSprites1[i], 'item' + str(i))) 
    treeSprites = loadSpritesheet('assets/trees1.png', 114, 100, xScale=gameScale, yScale=gameScale) #режем деревья Trees1.png на отдельные картинки-объекты
    for i in range(len(treeSprites)): #деревья также разбрасываем в случайные места на карте
        gameObjectList.append(gameObj([randrange(0, xRes-treeSprites[i].get_rect().w),randrange(0, yRes - treeSprites[i].get_rect().h)], treeSprites[i], 'a tree ' + str(i)))
    
    
    playerTextures = loadCharacterSpritesheet('assets/' + playerType + '.png', 32, 32, 10, 10, xScale=gameScale, yScale=gameScale, colorkey=-1)
    wallTextures = loadSpritesheet('assets/wall.png', 16, 32, xScale=gameScale, yScale=gameScale)
    ceilingTextures = loadSpritesheet('assets/ceiling.png', 16, 16, xScale=gameScale, yScale=gameScale)
    floorTextures = loadSpritesheet('assets/floor.png', 16, 16, xScale=gameScale, yScale=gameScale)



  

def loadLevel(tileData, decorationData, outputLevel):
    for y in range(0, 16):
        for x in range(0, 16):
            if tileData[y][x] == 'W':
                tile = Tile('wall', False)
                tile.image = choice(wallTextures)
                tile.offsetY = -16 * gameScale
            elif tileData[y][x] == 'c':
                tile = Tile('ceiling', True)
                tile.image = choice(ceilingTextures)
                tile.offsetY = 0
            else:
                tile = Tile('floor', True)
                tile.image = choice(floorTextures)
                tile.offsetY = 0
            if decorationData[y][x] == 'c':
                dec = Tile('ceiling', True)
                dec.image = choice(ceilingTextures)
                dec.offsetY = -16 * 2 * gameScale
            else:
                dec = None
            outputLevel.setTileAt(x, y, tile)
            outputLevel.setDecorationAt(x, y, dec)
            
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((xRes, yRes))
    pygame.display.set_caption('Roguelike')

    animationIndex, spriteIndex = 0, 0
    clock = pygame.time.Clock()
    player = Entity(level)

    loadTextures()
    loadLevel(tileData, decorationData, level)

    while True:
        clock.tick(24)

        player.isMoving = False
        player.dx, player.dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: return
        if keys[K_UP]:
            player.isMoving = True
            player.dy = -2 * gameScale
        if keys[K_DOWN]:
            player.isMoving = True
            player.dy = 2 * gameScale
        if keys[K_LEFT]:
            player.isFacingRight = False
            player.isMoving = True
            player.dx = -2 * gameScale
        if keys[K_RIGHT]:
            player.isFacingRight = True
            player.isMoving = True
            player.dx = 2 * gameScale
        if keys[K_z]:
            player.isCasting = True
            animationIndex = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        if animationIndex < 9:
            animationIndex += 1
        else:
            animationIndex = 0
            player.isCasting = False
            player.isMoving = False

        if player.isCasting:
            spriteIndex = 3
        elif player.isMoving:
            spriteIndex = 2
        else:
            spriteIndex = 0

        player.image, player.rect = playerTextures[spriteIndex][animationIndex]
        if not player.isFacingRight:
            player.image = pygame.transform.flip(player.image, True, False)
        
        pX, pY = player.update()
        for y in range(0, 16):
            for x in range(0, 16):
                screen.blit(level.getTileAt(x, y).image, (x * 16 * gameScale, y * 16 * gameScale + level.getTileAt(x, y).offsetY))
                if (level.getDecorationAt(x, y) is not None):
                    screen.blit(level.getDecorationAt(x, y).image, (x * 16 * gameScale, y * 16 * gameScale + level.getDecorationAt(x, y).offsetY))
                if ((x, y - 1) == (pX, pY)):
                    screen.blit(player.image, (player.x + player.offsetX, player.y + player.offsetY))

    #####################
        playerPos = (player.x + player.offsetX, player.y + player.offsetY) #позиция игрока
        for indx,_ in enumerate(gameObjectList):
            curObj = gameObjectList[indx]
            screen.blit(curObj.img, curObj.pos) #рисуем картинку каждого объекта на поверхность игрового экрана
            if (playerPos[1] + player.rect[3]) >= (curObj.pos[1] + curObj.lowestY): #если самая нижняя точка игрока объекта выше игрока
                screen.blit(player.image, playerPos) #рисуем игрока поверх объекта 



        pygame.display.flip()

if __name__ == '__main__': main()
