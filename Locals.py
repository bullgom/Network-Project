import os
dirPath = os.path.dirname(os.path.realpath(__file__))
from pygame.locals import USEREVENT
import math

"""Time Locals-----------------------------------------------------------------------------------------------------"""
LoginTimeout = 5000
LoginFailBoxShowTime = 5000
RegisterTimeout = 5000
RegisterFailBoxShowTime = 5000
RoomRefreshInterval = 1000
ReadyCancelBoxTime = 5000
GameEndTime = 5000
"""Userevent Locals-----------------------------------------------------------------------------------------------------"""
LoginTimeoutEvent = USEREVENT + 1
LoginFailBoxEvent = USEREVENT + 2
RegisterTimeoutEvent = USEREVENT + 3
RegisterFailBoxShowEvent = USEREVENT + 4
RoomRefreshEvent = USEREVENT + 5
StopRunning = USEREVENT + 6
StopReady = USEREVENT + 7
ReadyCanceledEvent = USEREVENT+ 8
GameEndEvent = USEREVENT + 9
"""Protocol Locals-----------------------------------------------------------------------------------------------------"""
LoginSuccessful = "loginsuccessful"
WrongUsernameOrPassword = "wrongusernameorpassword"
RegisterSuccessful = "registersuccessful"
RegisterFailed = "registerfailed"
MatchingSuccessful = "matchingsuccessful"
GameStart = "gamestart"
isMap = "ismap"
isCharacters = "ischaracters" #user and character match
GameEnd = "gameend"
Won = "won"
Lost = "lost"
DoraemonWon = "doraemonWon"
DoraemonLost = "doraemonLost"
"""Block Locals-----------------------------------------------------------------------------------------------------"""

SLOWVALUE = 0.9
QUICKENVALUE = 1.1
MULTIPLY = "multiply"

"""Anchor Locals-----------------------------------------------------------------------------------------------------"""

CENTER = 'center'
TOPLEFT = 'topleft'
BOTTOMLEFT = 'bottomleft'
TOPRIGHT = 'topright'
BOTTOMRIGHT = 'bottomright'
MIDTOP = 'midtop'
MIDLEFT = 'midleft'
MIDBOTTOM = 'midbottom'
MIDRIGHT = 'midright'

Anchors = [CENTER,TOPLEFT,MIDTOP,TOPRIGHT,MIDLEFT,MIDRIGHT,BOTTOMLEFT,MIDBOTTOM,BOTTOMRIGHT]



"""Character Locals--------------------------------------------------------------------------------------------------"""
West = "west"
East = "east"
North = "north"
South = "south"
NE = "northeast"
SE = "southeast"
NW = "northwest"
SW = "southwest"
sin45 = math.sin(45)
cos45 = math.sin(45)


"""Map Locals                         """
_SimpleMap = "simplemap"