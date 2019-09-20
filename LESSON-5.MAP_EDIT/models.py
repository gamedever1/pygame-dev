# -*- coding: utf-8 -*-
import pygame


####### GAME OBJECTS ###########
class GameWorld():
    def __init__(self):
        self.edit_mode = None
        self.show_rects = False

class GameObject():
    def __init__(self, pos, obj_image, obj_props={}):
        self.pos = pos #позиция объекта на карте x,y
        self.img = obj_image #картинка объекта
        self.obj_props=obj_props ### множество параметров объекта с их значениями
        
        self.follow_mouse = False #следовать ли за указателем мыши
        self.follow_mouse_offset = [0,0] #смещения указателя мыши от нулевый координат объекта
        
        obj_image_rect = obj_image.get_rect()
        self.img_rect = obj_image_rect #получение прямоугольной Rect(x=0,y=0,w,h) картинки        
        colorkey = obj_image.get_at((0, 0)) #берет цвет самого верхнего левого пикселя
        self.img.set_colorkey(colorkey) #устанавливает этот цвет как цвет прозрачности
        self.img_mask = pygame.mask.from_surface(obj_image) # по colorkey-цвету прозрачности создает маску(непрозрачных пикелей)

        self.update_img_rect()
        self.calc_rects()
    
    def set_position(self, newPosition): # Изменить позицию объекта
        self.pos[0] = newPosition[0] 
        self.pos[1] = newPosition[1] 
        self.update_img_rect() 
        
    def update_img_rect(self): # Обновить прямоугольник объекта с учетом позиции
        self.img_rect.x = self.pos[0] #устанавливает в прямоугольнике x-координату объекта 
        self.img_rect.y = self.pos[1] #и y-координату            
    
    def calc_rects(self): ### Расчет непрозрачной области и области коллизий
        obj_image_rect = self.img.get_rect() #
        
## РАСЧЕТ ПРЯМОУГОЛЬНОЙ ОБЛАСТИ ОБЪЕКТА БЕЗ ПРОЗРАЧНЫХ ПИКСЕЛЕЙ ##          
        leftmostX = obj_image_rect.w 
        rightmostX = 0 
        topY = obj_image_rect.h 
        lowY = 0 
        for imgY in range(obj_image_rect.h): #расчет прямоугольника, в который вписана картинка объект без прозрачных областей 
            for imgX in range(obj_image_rect.w):
                if (self.img_mask.get_at((imgX, imgY))) == 1: 
                    if imgY < topY: 
                        topY = imgY 
                    if imgY > lowY: 
                        lowY = imgY 
                    if imgX < leftmostX: 
                        leftmostX = imgX 
                    if imgX > rightmostX: 
                        rightmostX = imgX 
        self.opaq_rect = pygame.Rect(leftmostX, topY, rightmostX - leftmostX, lowY - topY) #opaq_rect - проямоугольник вокруг непрозрачных пикселей 
        
        self.lowestY = lowY # Y-координата самого нижнего непрозрачного пикселя в картинке объекта


## РАСЧЕТ ОБЛАСТИ КОЛЛИЗИЙ ##        
        leftmostX = obj_image_rect.w 
        rightmostX = 0 
        topY = obj_image_rect.h 
        
        imgY = lowY 
        scanHeight = 15 
        while (imgY >= 0 and scanHeight > 0): #расчет прямоугольника для коллизий
            for imgX in range(obj_image_rect.w): 
                if (self.img_mask.get_at((imgX, imgY))) == 1: 
                    if imgY < topY: 
                        topY = imgY 
                    if imgY > lowY: 
                        lowY = imgY  
                    if imgX < leftmostX: 
                        leftmostX = imgX 
                    if imgX > rightmostX: 
                        rightmostX = imgX  
            imgY -= 1 
            scanHeight -= 1 
        self.coll_rect = pygame.Rect(leftmostX, topY, rightmostX - leftmostX, lowY - topY) #coll_rect - проямоугольник внизу объекта для расчета стоклновений   

##### TEXT OBJECTS ######
class TextObject(): # объекты, которые создаются при необходимости нарисовать текст на экране игры
    def __init__(self, pos, text_str, text_color, exist_time=-1, font_size=24, font_name=None ):
        self.pos = pos #положение на экране
        self.text_str = text_str #строка текста
        self.text_color = text_color
        self.alpha = 255 #прозрачность
        self.exist_time = exist_time #время существования текста до удаления, если -1, то текст постоянный
        self.text_visible = True #показывать или не показывать этот текст
        self.font_name = font_name #шрифт
        self.font_size = font_size #размер шрифта




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
        





