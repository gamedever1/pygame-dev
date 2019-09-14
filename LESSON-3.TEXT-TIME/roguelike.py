#/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Horizontal collision detection, everything else

import os, pygame
from pygame.locals import *
from random import randint, choice, randrange 
from utils import loadSpritesheet, loadCharacterSpritesheet
from models import Level, Tile, Entity ### убираем свои нвоые классы из этой строки
import models ### обращаться к своим новым классам будем через models.class
import time ### библиотека для работы с временем

#### НОВЫЕ ПЕРЕМЕННЫЕ
gameObjectList = [] ### глобальная переменная со всеми объектами в игре, сначала пустой список
textObjectList = [] ### список текстовых объектов
#### НОВЫЕ ПЕРЕМЕННЫЕ

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

    items1_Names = ['Ящик', 'Открый ящик', 'Сундук', 'Открый сундук', 'Бочка', 'Открытая бочка', 'Мешочек', 'Мешок', 'Большой мешок'] ###список с именами объектов в таком же порядке, как в tileset-картинке
    itemSprites1 = loadSpritesheet('assets/Items1.png', 16, 32, xScale=gameScale, yScale=gameScale) #режем вещи Items1.png на отдельные картинки-объекты
    for i in range(len(itemSprites1)): #для каждой нарезанной картинки-объекта, помещаем его в случайное место на карте
        gameObjectList.append(models.gameObj([randrange(0, xRes-itemSprites1[i].get_rect().w),randrange(0, yRes - itemSprites1[i].get_rect().h)], itemSprites1[i], items1_Names[i])) 
    treeSprites = loadSpritesheet('assets/trees1.png', 114, 100, xScale=gameScale, yScale=gameScale) #режем деревья Trees1.png на отдельные картинки-объекты
    for i in range(len(treeSprites)): #деревья также разбрасываем в случайные места на карте
        gameObjectList.append(models.gameObj([randrange(0, xRes-treeSprites[i].get_rect().w),randrange(0, yRes - treeSprites[i].get_rect().h)], treeSprites[i], 'Дерево'))   
    
    gameObjectList.sort(key=lambda x: x.pos[1]+x.lowestY) #сортируем массив объектов по ключу самого 

    playerTextures = loadCharacterSpritesheet('assets/' + playerType + '.png', 32, 32, 10, 10, xScale=gameScale, yScale=gameScale, colorkey=-1)
    wallTextures = loadSpritesheet('assets/wall.png', 16, 32, xScale=gameScale, yScale=gameScale)
    ceilingTextures = loadSpritesheet('assets/ceiling.png', 16, 16, xScale=gameScale, yScale=gameScale)
    floorTextures = loadSpritesheet('assets/floor.png', 16, 16, xScale=gameScale, yScale=gameScale)



###    

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

        mouse_pressed1, mouse_pressed2, mouse_pressed3 = pygame.mouse.get_pressed() ### получаем состояние нажатых на мышке кнопок

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

#### ОБРАБОТКА НАЖАТИЙ КЛАВИАТУРЫ И МЫШИ ####
        for event in pygame.event.get(): ### добавляем свой функционал в цикл получения сообщений от мыши и клавиатуры   
            if event.type == MOUSEBUTTONDOWN: ### если произошло событие - нажатие кнопки мыши
                    mouse_pos = event.pos ### Получаем x,y координаты мыши на экране игры
                    for curObj in gameObjectList: ### Для всех объектов проверяем попадение курсора мыши в этот объект
                        pos_in_mask = mouse_pos[0] - curObj.img_rect.x, mouse_pos[1] - curObj.img_rect.y ### вычисление позиции курсора относительно координат маски прозрачности объекта
                        if curObj.img_rect.collidepoint(mouse_pos) and curObj.img_mask.get_at(pos_in_mask) == 1: ### проверяем, находится ли мышь на каком-то объекте, и прозрачен ли пиксель, на котором находится указатель мыши
                            new_time_obj = models.textObj([mouse_pos[0],mouse_pos[1]], curObj.objName, (255,255,255) ,1500) ### Создаем текстовый объект с координатами указателя мыши, текстом, равным имени объекта под мышкой, белым цветом шрифта(255,255,255) и временем существования 1500 миллисеукнд
                            new_time_obj.time1 = time.time() ### в свойство текстового объекта time1 заносим время, когда этот текст создан                            
                            textObjectList.append(new_time_obj) ### Добавляем новую надпись(текстовый объект) в список всех надписей
                            break ### после первого найденного объекта под мышью, выходим из цикла, чтобы не появлялось несколько надписей в одном месте

            
            elif event.type == QUIT:
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

#### ОТРИСОВКА ОБЪЕКТОВ ####
        playerPos = (player.x + player.offsetX, player.y + player.offsetY) #позиция игрока на карте x,y
        for indx,_ in enumerate(gameObjectList): #в массиве всех созданным нами объектов
            curObj = gameObjectList[indx]
            screen.blit(curObj.img, curObj.pos) #рисуем картинку каждого объекта на поверхность игрового экрана
            if (playerPos[1] + player.rect[3]) >= (curObj.pos[1] + curObj.lowestY): #если самая нижняя точка игрока объекта выше игрока
                screen.blit(player.image, playerPos) #рисуем игрока поверх объекта
                 
#### ОТРИСОВКА ТЕКСТА ####
            for indx,_ in enumerate(textObjectList): ### перечисляем все надписи(текстовые объекты из их общего списка)
                textObj = textObjectList[indx] ### работаем с самим объектом, а не копией, как в случае просто for цикла, чтобы не тратить лишнюю память
                if textObj.textVisible == False: ### Если в объекте указана невидимость
                    continue ### пропускаем этот объект
                textSurf = pygame.font.SysFont(textObj.fontName, textObj.fontSize).render(textObj.text_str, False, textObj.text_color) ### рисуем текст(создаем поверхность Surface с текстом)
                screen.blit( textSurf, textObj.pos ) ### накладываем поверхность с нарисованным текстом на поверхность экрана, выводя текст на игровой экран
                if textObj.exist_time != -1: ### если у надписи указано время существования(exist_time)
                    elapsed = (time.time() - textObj.time1)*1000 ###проверяем сколько миллисекунд прошло со времени создания надписи
                    if elapsed > textObj.exist_time: ### если прошло больше времени, чем указано во времени существования (exist_time)
                        textObjectList.pop(indx) ### удаляем объект из списка надписей
                        
            
            

        pygame.display.flip()

if __name__ == '__main__': main()
