from Block import *
from Location import *

class Map():
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos
        self.rect = pyg.Rect(pos,size)
        self.locations = []
        self.blocks = []

    def setStartLocation(self, x, y):
        location = Location((x, y), (50,50), 0)
        self.locations.append(location)

    def setDoraemonStartLocation(self, x, y):
        location = Location((x,y), (50,50), 1)
        self.locations.append(location)

    def addLocation(self, location):
        for i in self.locations:
            if i.id == location.id:
                raise ValueError("Location id is already taken")

        self.locations.append(location)

    def addBlock(self,block):
        self.blocks.append(block)

    def update(self, character):

        for location in self.locations:
            if location.Rect.colliderect(character.hitbox):
                if location.action != None:
                    if location.takeArg == True:
                        location.action(character)
                    else:
                        location.action()
        for block in self.blocks:
            if block.level > 0:
                if block.rect.colliderect(character.hitbox):
                    character.pos.x -= character.xVel
                    character.pos.y -= character.yVel
            elif block.level < 0:
                if not block.rect.contains(character.hitbox):
                    character.pos.x -= character.xVel
                    character.pos.y -= character.yVel

    def render(self,surface):
        for block in self.blocks:
            block.render(surface)