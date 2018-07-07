import pygame as pyg
import threading
from NETWORKPROJECT.Locals import *
import math

class Character():
    def __init__(self, pos, size, hitbox, imageDir, name, speed, isAlive=True):
        self.pos = pos
        self.size = size
        self.rect = pyg.Rect(pos,size)
        self._hitbox = hitbox
        self._image = pyg.image.load(imageDir).convert_alpha()
        self._image = pyg.transform.scale(self._image, self.size)
        self.name = name
        self.xVel = 0
        self.yVel = 0
        self.moveSpeed = speed
        self.currentMoveSpeed = speed
        self.isAlive = isAlive

    @property
    def hitbox(self):
        return self._hitbox

    @hitbox.setter
    def hitbox(self,value):
        if not isinstance(value, pyg.Rect):
            raise TypeError("Value must be a Rect type")

        self._hitbox = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self,directory):
        self._image = pyg.image.load(directory).convert_alpha()

    def _setMoveSpeed(self, value, flag = None):
        assert type(flag) is (str or None), "Flag must be a string or a None type"
        if(flag == None):
            self.currentMoveSpeed = value
        elif(flag == "increment"):
            self.currentMoveSpeed = self.moveSpeed + value
        elif(flag == "decrement"):
            self.currentMoveSpeed = self.moveSpeed - value
        elif(flag == "multiply"):
            self.currentMoveSpeed = self.moveSpeed*value

    def setMoveSpeed(self, value, flag = None, time = None):
        if(time != None):
            self._setMoveSpeed(value, flag)
            if(flag == None):
                timer = threading.Timer(time, self._setMoveSpeed, self.moveSpeed)
            elif(flag == "increment"):
                timer = threading.Timer(time, self._setMoveSpeed, (value, "decrement"))
            elif(flag == "decrement"):
                timer = threading.Timer(time, self._setMoveSpeed, (value, "increment"))
            elif(flag == "multiply"):
                timer = threading.Timer(time, self._setMoveSpeed, (1/value, "multiply"))
            timer.start()
        else:
            self._setMoveSpeed(value, flag)

    def move(self, direction=None):
        if direction == North:
            self.yVel = -1 * self.currentMoveSpeed
            self.xVel = 0
        elif direction == NE:
            self.yVel = -1 * (self.currentMoveSpeed * sin45)
            self.xVel = (self.currentMoveSpeed * cos45)
        elif direction == East:
            self.yVel = 0
            self.xVel = self.currentMoveSpeed
        elif direction == SE:
            self.yVel = (self.currentMoveSpeed * sin45)
            self.xVel = (self.currentMoveSpeed * cos45)
        elif direction == South:
            self.yVel = self.currentMoveSpeed
            self.xVel = 0
        elif direction == SW:
            self.yVel = (self.currentMoveSpeed * sin45)
            self.xVel = -1 * self.currentMoveSpeed * cos45
        elif direction == West:
            self.yVel = 0
            self.xVel = -1 * self.currentMoveSpeed
        elif direction == NW:
            self.yVel = -1 * self.currentMoveSpeed * sin45
            self.xVel = -1 * self.currentMoveSpeed * cos45
        else:
            self.yVel = 0
            self.xVel = 0
        self.pos.x += self.xVel
        self.pos.y += self.yVel

    def render(self,surface):
        surface.blit(self.image, self.rect)



















