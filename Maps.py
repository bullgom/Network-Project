from Map import *
from Location import Location
from Block import *
import pygame as pyg
"""Map Locals-----------------------------------------------------------------------------------------------------"""

SimpleMap = Map((0,0),(1280,720))
SimpleMap.setStartLocation(100,100)
SimpleMap.setDoraemonStartLocation(1180, 620)
def teleport1(character):
    character.pos.x = 1265
    character.pos.y = 360

def teleport2(character):
    character.pos.x = 15
    character.pos.y = 360

l1 = Location((10, 360),(20,100),2)
l1.action = teleport1
l1.takeArg = True
SimpleMap.addLocation(l1)
b1 = Block((0,0),(1280,720),"Ground",0,dirPath+r"/resources/ground.png",-1,anchor=TOPLEFT)
b2 = Block((640,360),(200,30),"Wall",1,dirPath+r"/resources/wall.png",1,anchor=CENTER)
SimpleMap.addBlock(b1)
SimpleMap.addBlock(b2)