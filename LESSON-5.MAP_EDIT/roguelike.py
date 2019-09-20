#/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Horizontal collision detection, everything else

import os, pygame
from pygame.locals import *
from random import randint, choice, randrange 
from utils import loadSpritesheet, loadCharacterSpritesheet
from models import Level, Tile, Entity # убираем свои новые классы из этой строки
import models # обращаться к своим новым классам будем через models.class
import time # библиотека для работы с временем
import json ### библиотке для работы с JSON

## НОВЫЕ ПЕРЕМЕННЫЕ
gameObjectList = [] # глобальная переменная со всеми объектами в игре, сначала пустой список
textObjectList = [] # список текстовых объектов
World = models.GameWorld() ### Создаем объект состояния игрового мира
white_color = (255,255,255) ### белый цвет
## НОВЫЕ ПЕРЕМЕННЫЕ

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
    
    assets_dict = {} ### словарь с именем asset-картинки и соответствующим ей списком картинок
    game_objects_json = "[{\"posX\": 281, \"posY\": 162, \"obj_props\": {\"ObjectName\": \"big bag\", \"CanMove\": \"True\", \"asset_index\": 8, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 249, \"posY\": 172, \"obj_props\": {\"ObjectName\": \"barrel\", \"asset_index\": 4, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 324, \"posY\": 190, \"obj_props\": {\"ObjectName\": \"open chest\", \"asset_index\": 1, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 234, \"posY\": 192, \"obj_props\": {\"ObjectName\": \"small bag\", \"CanMove\": \"True\", \"asset_index\": 6, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 116, \"posY\": 64, \"obj_props\": {\"ObjectName\": \"Tree\", \"asset_index\": 1, \"asset_name\": \"assets/trees1.png\"}, \"height\": 200, \"width\": 228}, {\"posX\": 312, \"posY\": 70, \"obj_props\": {\"ObjectName\": \"Tree\", \"asset_index\": 0, \"asset_name\": \"assets/trees1.png\"}, \"height\": 200, \"width\": 228}, {\"posX\": 242, \"posY\": 231, \"obj_props\": {\"ObjectName\": \"chest\", \"asset_index\": 2, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 329, \"posY\": 240, \"obj_props\": {\"ObjectName\": \"box\", \"asset_index\": 0, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 87, \"posY\": 93, \"obj_props\": {\"ObjectName\": \"Tree\", \"asset_index\": 5, \"asset_name\": \"assets/trees1.png\"}, \"height\": 200, \"width\": 228}, {\"posX\": 315, \"posY\": 264, \"obj_props\": {\"ObjectName\": \"bag\", \"CanMove\": \"True\", \"asset_index\": 7, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 255, \"posY\": 264, \"obj_props\": {\"ObjectName\": \"open barrel\", \"asset_index\": 5, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 284, \"posY\": 271, \"obj_props\": {\"ObjectName\": \"open chest\", \"asset_index\": 3, \"asset_name\": \"assets/Items1.png\"}, \"height\": 64, \"width\": 32}, {\"posX\": 323, \"posY\": 125, \"obj_props\": {\"ObjectName\": \"Tree\", \"asset_index\": 4, \"asset_name\": \"assets/trees1.png\"}, \"height\": 200, \"width\": 228}]"
    list_from_json = json.loads(game_objects_json) ### загружаем json-описание всех объектов
    for obj in list_from_json: ### для каждого из объектов
        asset_name = obj['obj_props']['asset_name'] ### имя файла asset-картинки 
        asset_index = obj['obj_props']['asset_index'] ### индекс картинки в asset-e, которая соответствует данному объекту 
        if asset_name not in assets_dict: ### если такого имени файла нет в словаре asset-ов, добавляем, если уже есть, пропускаем добавление
            assets_dict[asset_name] = loadSpritesheet(asset_name, int(obj['width']/gameScale), int(obj['height']/gameScale), xScale=gameScale, yScale=gameScale)
        cur_sprite = assets_dict[asset_name][asset_index] ### картинка текущего объекта - берем из asset-а по индексу 
        gameObjectList.append(models.GameObject([obj['posX'],obj['posY']], cur_sprite, obj['obj_props'])) ### добавляем в список всех игровых объектов

    gameObjectList.sort(key=lambda x: x.pos[1]+x.lowestY) #сортируем массив объектов по ключу самого нижнего

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



        mouse_pos = pygame.mouse.get_pos() # получение координат указателя мыши
## ОБРАБОТКА НАЖАТИЙ КЛАВИАТУРЫ И МЫШИ ##
        for event in pygame.event.get(): # добавляем свой функционал в цикл получения сообщений от мыши и клавиатуры   
            if event.type == MOUSEBUTTONDOWN: # если произошло событие - нажатие кнопки мыши
                    #mouse_pos = event.pos # Получаем x,y координаты мыши на экране игры
                    for cur_obj in gameObjectList: # Для всех объектов проверяем попадение курсора мыши в этот объект
                        pos_in_mask = mouse_pos[0] - cur_obj.img_rect.x, mouse_pos[1] - cur_obj.img_rect.y # вычисление позиции курсора относительно координат маски прозрачности объекта
                        if cur_obj.img_rect.collidepoint(mouse_pos) and cur_obj.img_mask.get_at(pos_in_mask) == 1: # проверяем, находится ли мышь на каком-то объекте, и прозрачен ли пиксель, на котором находится указатель мыши
                            cur_obj_name = 'unnamed' ### имя объекта, по-умолчанию безымянный
                            if 'ObjectName' in cur_obj.obj_props: ### если в словаре есть свойство ИмяОбъекта
                                cur_obj_name = cur_obj.obj_props["ObjectName"] ### создаем надпись с этим именем
                            new_text_obj = models.TextObject([mouse_pos[0],mouse_pos[1]], cur_obj_name, white_color ,1500) # Создаем текстовый объект с координатами указателя мыши, текстом, равным имени объекта под мышкой, белым цветом шрифтаwhite_color и временем существования 1500 миллисеукнд
                            new_text_obj.time1 = time.time() # в свойство текстового объекта time1 заносим время, когда этот текст создан                            
                            
                            if pygame.mouse.get_pressed()[2]: ### если нажата ПРАВАЯ кнопка мыши
                                textObjectList.append(new_text_obj) # Добавляем новую надпись(текстовый объект) в список всех надписей
                            else: ### если нажата ЛЕВАЯ кнопка мыши, захватываем объект
                                cur_obj.follow_mouse = True # устанавливаем флаг следования за мышкой(захватываем объект мышкой)
                                cur_obj.follow_mouse_offset = [mouse_pos[0] - cur_obj.pos[0], mouse_pos[1] - cur_obj.pos[1]] # смещение мышки относительно нулевых координат области объекта
                            
                            break # после первого найденного объекта под мышкой, выходим из цикла, чтобы не появлялось несколько надписей в одном месте

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e: ### Если на клавитуре нажата клавиша 'e'
                    if World.edit_mode == None: ### Включаеv режим EDIT(Редактирования объектов)
                        mode_text_obj = models.TextObject([10,10], "EDIT", white_color, -1, 40) ### создаем надпись слева вверху
                        textObjectList.append(mode_text_obj) ### Добавляем надпись в список всех текстовых объектов
                        World.edit_mode = textObjectList[len(textObjectList) - 1]
                    else: ### Если режим Редактирования уже включен,
                        textObjectList.remove(World.edit_mode) ### Удаляем надпись 
                        World.edit_mode = None ### Отменяем режим Редактирования(EDIT)
                        ## При выключении режима редактирования, выводим в консоль все объекты
                        all_objects_dict = [] ###список со всеми объектами
                        for i in range(len(gameObjectList) - 1): ### Для всех оюъектов в игре
                            cur_obj = gameObjectList[i] ###текущий объект
                            new_obj_dict = {'obj_props' : cur_obj.obj_props, ### все свойства объекта заносим во вложенный словарь
                                            'posX' : cur_obj.pos[0], ### Позиция X
                                            'posY' : cur_obj.pos[1], ### Позиция Y
                                            'width' : cur_obj.img_rect.w, ### Ширина картинки
                                            'height' : cur_obj.img_rect.h ### Высота картинки
                                            }
                            all_objects_dict.append(new_obj_dict) ### добавляем новый объект с описанием в список всех объектов 
                        json_dump = json.dumps(all_objects_dict) ### выгружаем описание всех объектов игры в json-формате
                        print(json.dumps(json_dump)) ### выводим полученный json в консоль
                elif event.key == pygame.K_r: ### Постоянное отображение рамок все объектов
                    if World.show_rects: ### Если включено
                        World.show_rects = False ### выключаем режим
                    else: ### включаем, если отключено
                        World.show_rects = True
            
            
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

## ОТРИСОВКА ОБЪЕКТОВ ##
        player_pos = (player.x + player.offsetX, player.y + player.offsetY) #позиция игрока на карте x,y
        for indx,_ in enumerate(gameObjectList): #в массиве всех созданным нами объектов
            cur_obj = gameObjectList[indx]
            if cur_obj.follow_mouse: # Если установлен флаг следования за мышкой (объект взят) 
                if World.edit_mode != None or ('CanMove' in cur_obj.obj_props and cur_obj.obj_props['CanMove'] == 'True'): ### Если включен режим редактирования(EDIT)
                     # получение состояния нажатия всех кнопок мыши
                    if pygame.mouse.get_pressed()[0]: # проверяем, нажата ли ЛЕВАЯ кнопка мыши
                        newPosX = mouse_pos[0] - cur_obj.follow_mouse_offset[0] # высчитываем новую позицию с учетом смещения X-координату
                        newPosY = mouse_pos[1] - cur_obj.follow_mouse_offset[1] # Y-координату
                        cur_obj.set_position([newPosX,newPosY]) # при зажатой кнопке мыши, переносим объект на текущую позицию мыши
                    else: # если левая кнопка отпущена, бросаем предмет
                        cur_obj.follow_mouse = False # отключаем следование за мышью(бросаем объект)
                        gameObjectList.sort(key=lambda x: x.pos[1]+x.lowestY) # снова сортируем объекты в правильном порядке по самому нижнему пикселю
                                                   
            screen.blit(cur_obj.img, cur_obj.pos) #рисуем картинку каждого объекта на поверхность игрового экрана
            
            if World.show_rects or (World.edit_mode != None and cur_obj.follow_mouse): ### Если включен режим Редактирования(EDIT), рисуем прямоугольники, очерчивающие непрозрачную область объекта и прямоугольник для коллизий
                opq_rect = pygame.Rect(cur_obj.pos[0]+cur_obj.opaq_rect[0], cur_obj.pos[1]+cur_obj.opaq_rect[1], cur_obj.opaq_rect[2], cur_obj.opaq_rect[3]) ### расчет прямоугольника для отображения на игровом экране
                pygame.draw.rect(screen, white_color, opq_rect, 1) ### рисуем рамку объекта 
                col_rect = pygame.Rect(cur_obj.pos[0]+cur_obj.coll_rect[0], cur_obj.pos[1]+cur_obj.coll_rect[1], cur_obj.coll_rect[2], cur_obj.coll_rect[3])
                pygame.draw.rect(screen, (100,255,0), col_rect, 2) ### зеленым цветом рисуем область коллизий данного объекта

                
            if (player_pos[1] + player.rect[3]) >= (cur_obj.pos[1] + cur_obj.lowestY): #если самая нижняя точка игрока объекта выше игрока
                screen.blit(player.image, player_pos) #рисуем игрока поверх объекта
                
        if World.edit_mode != None: ### Если режим EDIT
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player.rect[2], player.rect[3]) ### Расчитываем прямоугольник вокруг игрока
            pygame.draw.rect(screen, (0,0,255), player_rect, 2) ### рисуем рамку игрока
                 
## ОТРИСОВКА ТЕКСТОВЫХ ОБЪЕКТОВ ##
        for indx,_ in enumerate(textObjectList): # перечисляем все надписи(текстовые объекты из их общего списка)
            text_obj = textObjectList[indx] # работаем с самим объектом, а не копией, как в случае просто for цикла, чтобы не тратить лишнюю память
            if text_obj.text_visible == False: # Если в объекте указана невидимость
                continue # пропускаем этот объект
            text_surface = pygame.font.SysFont(text_obj.font_name, text_obj.font_size).render(text_obj.text_str, False, text_obj.text_color) # рисуем текст(создаем поверхность Surface с текстом)
            screen.blit( text_surface, text_obj.pos ) # накладываем поверхность с нарисованным текстом на поверхность экрана, выводя текст на игровой экран
            if text_obj.exist_time != -1: # если у надписи указано время существования(exist_time)
                elapsed = (time.time() - text_obj.time1)*1000 #проверяем сколько миллисекунд прошло со времени создания надписи
                if elapsed > text_obj.exist_time: # если прошло больше времени, чем указано во времени существования (exist_time)
                    textObjectList.pop(indx) # удаляем объект из списка надписей
                        
            
            

        pygame.display.flip()

if __name__ == '__main__': main()
