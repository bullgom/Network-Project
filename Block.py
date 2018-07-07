import pygame as pyg
from GUI.base import BaseWidget
from Locals import *

class Block(BaseWidget):
    def __init__(self, pos, size, name, id, imageDirectory, level, anchor=CENTER):
        super().__init__(pos,size,anchor=anchor)
        self.name = name
        self.id = id
        self.image = pyg.image.load(imageDirectory).convert_alpha()
        self.image = pyg.transform.scale(self.image,size)

        self.level = level #If level < 0 then lower than character

    def render(self, surface):
        surface.blit(self.image, self.as_rect())