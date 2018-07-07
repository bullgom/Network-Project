import pygame as pyg
from Locals import *
from GUI.base import *

class Location():
    def __init__(self, pos, size, id, action=None,takeArg=False,anchor=CENTER):
        self._id = id
        self.action = action
        self.takeArg = takeArg
        self.arg = None

        self.rect = pyg.Rect(pos,size)
        self._anchor = anchor
        self._pos = pos
        self._size = size

    def __contains__(self, item):
        return self.left <= item[0] <= self.right and self.top <= item[1] <= self.bottom

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")

        self._id = value

    @property
    def anchor(self):
        if callable(self._anchor):
            return self._anchor()
        else: return self._anchor

    @anchor.setter
    def anchor(self, value):
        if not callable(value):
            if value not in (Anchors):
                raise ValueError
        self._anchor = value

    @property
    def size(self):
        if callable(self._size):
            return self._size()
        else: return self._size

    @size.setter
    def size(self, value):
        if not callable(value):
            if isinstance(value, tuple):
                raise TypeError("The size must be a callable that returns 2-tuples or a 2-tuple")
            elif len(value) != 2:
                raise TypeError("The size must be a callable that returns 2-tuples or a 2-tuple")
        self._size = value

    @property
    def pos(self):
        if callable(self._pos):
            return self._pos()
        else: return self._pos

    @pos.setter
    def pos(self, value):
        if not callable(value):
            if isinstance(value, tuple):
                raise TypeError("The pos must be a callable that returns 2-tuples or a 2-tuple")
            elif len(value) != 2:
                raise TypeError("The pos must be a callable that returns 2-tuples or a 2-tuple")
        self._pos = value

    def as_rect(self):
        return self.pos, self.size