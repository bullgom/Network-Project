import pygame as pyg
pyg.init()
pyg.display.set_mode((1,1))
from mainFile import DoraemonTag
title = "DoraemonTagGame"
screenSize = (1500,1000)
fpsLimit = 60

if __name__ == "__main__":
    Game = DoraemonTag(title,screenSize,fpsLimit)
    Game.run()