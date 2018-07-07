from GUI.base import *
from NETWORKPROJECT.Locals import *
import pygame as pyg

class ImageBox(BaseWidget):
    def __init__(self, pos, size, directory, anchor = CENTER):
        super().__init(pos, size, anchor)
        surface = pyg.image.load(imageDirectory).convert_alpha()
        self._image = pyg.transform.scale(surface, self.size)

    @property
    def image(self):
        if callable(self._image):
            return self._image()
        else: return self._image

    @image.setter
    def image(self, directory):
        if not isinstance(directory, str):
            raise TypeError("Directory must be str type." + " Got " + type(directory) + " indtead.")

        surface = pyg.image.load(directory).convert_alpha()
        self._image = pyg.transform.scale(surface, self.size)

    @BaseWidget.size.setter
    def size(self, value):
        self.size = value
        self._image = pyg.transform.scale(self.image, value)

    def render(self, surf):
        surf.blit(self.image, self.size)
