import pygame as pyg
import os, copy
from pygame.locals import *
from GUI.locals import *
from GUI import SimpleText, InLineTextBox, InLinePassBox, FocusSelector, Font
from GUI import Separator as Sep
from ImageBox import *
from buttons import *
from Mastermind import *
from Maps import *
from messageHandler import *
from User import *
from _thread import start_new_thread


class DoraemonTag():
    def __init__(self, title, screenSize, fpsLimit):
        pyg.init()
        pyg.font.init()
        self.title = title
        self.screenSize = screenSize
        self.fpsLimit = fpsLimit

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pyg.display.set_mode(self.screenSize, DOUBLEBUF)

        self.clock = pyg.time.Clock()
        self.running = False

        self.ip = 'localhost'
        self.port = 7699
        self._user = None
        self.handler = messageHandler(self.ip, self.port)
        self.characterID = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self,value):
        if not isinstance(value, User):
            raise TypeError("Value must be User type")
        self._user = value

    def newWindow(self):
        self.screen = pyg.display.set_mode(self.screenSize, DOUBLEBUF | NOFRAME)

    def stopGame(self):
        pyg.quit()
        sys.exit()

    def run(self):
        self.loginScreen()
        loggedin = True
        while(loggedin):
            self.gameStartScreen()
            self.game()

    def loginScreen(self):
        MyFont = Font(20,file= dirPath + r"/WHOOPASS.TTF")

        IDTextBox = SimpleText("  I   D  ", (int(self.screenSize[0] / 2), int(self.screenSize[1] * 2/ 3)),
                               color = WHITE, bg_color= NAVY, anchor= TOPRIGHT, font=MyFont)
        PasswordTextBox = SimpleText(" PASSWORD ", IDTextBox.bottomleft + Sep(0, 2),
                               color = WHITE, bg_color= NAVY, anchor= TOPLEFT, font=MyFont)
        IDInputBox = InLineTextBox(IDTextBox.topright + Sep(2 , 0), 100,
                                   BLACK, WHITE,anchor=TOPLEFT)
        PasswordInputBox = InLinePassBox(PasswordTextBox.topright + Sep(2, 0),
                                         100, BLACK, WHITE, anchor= TOPLEFT)
        buttonSize = (20,75)
        LoginButton = Button(self.login, (int(self.screenSize[0] / 2), int(self.screenSize[1] * 4 / 5)), (150,30),
                             "Login", color= BLACK, takeArg=True, flags=BaseButton.THREADED_CALL | BaseButton.CALL_ON_PRESS)
        QuitButton = Button(self.stopGame, LoginButton.topright + Sep(5, 0),(150,30),
                            "Quit", color=BLACK, anchor=TOPLEFT)
        RegisterButton = Button(self.registerScreen, LoginButton.topleft + Sep(5, 0),(150,30),
                                "Register", color=BLACK, anchor=TOPRIGHT)

        LoginFailBox = SimpleText("Login Failed",(10,10), RED, WHITE, anchor=TOPLEFT)

        renderList = [IDInputBox,IDTextBox,PasswordInputBox,PasswordTextBox,LoginButton,QuitButton,RegisterButton]
        focus = FocusSelector(IDInputBox, PasswordInputBox)
        focus.select(0)

        running = True
        while running:
            self.clock.tick(self.fpsLimit)
            mouse = pyg.mouse.get_pos()

            LoginButton.set_arg((IDInputBox.text, PasswordInputBox.text))

            for event in pyg.event.get():
                focus.selected().update(event)
                LoginButton.update(event)
                QuitButton.update(event)
                RegisterButton.update(event)

                if event.type == QUIT:
                    self.stopGame()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if IDInputBox.text != "" and PasswordInputBox.text != "":
                            self.login(IDInputBox.text, PasswordInputBox.text)
                    elif event.key == K_TAB:
                        if event.mod & KMOD_SHIFT:
                            focus.prev()
                        else:
                            focus.next()

                elif event.type == MOUSEBUTTONDOWN:
                    if mouse in IDInputBox:
                        focus.select(IDInputBox)
                    elif mouse in PasswordInputBox:
                        focus.select(PasswordInputBox)

                elif event.type == LoginFailBoxEvent:
                    renderList.remove(LoginFailBox)

                if event.type == LoginTimeoutEvent:
                    self.handler.receiveStop()

            while not(self.handler.received.empty()):
                message = self.handler.received.get()
                print(message)
                if message == LoginSuccessful:
                    self.handler.receiveStop()
                    return
                if message == WrongUsernameOrPassword:
                    self.handler.receiveStop()
                    pyg.time.set_timer(LoginFailBoxEvent, LoginFailBoxShowTime)
                    renderList.append(LoginFailBox)

            self.screen.fill(WHITE)
            for item in renderList:
                item.render(self.screen)

            pyg.display.update()
            pyg.display.flip()

    def login(self, id, password):
        pyg.time.set_timer(LoginTimeoutEvent,5000)
        data = ("LOGIN", id, password)
        print(data)
        self.handler.client.send(data)
        self.handler.receiveStart(num=1)


    def cancel(self, event):
        pyg.time.set_timer(event,100)

    def registerScreen(self):
        MyFont = Font(20,file= dirPath + r"/WHOOPASS.TTF")
        background = ImageBox((0, 0), self.screenSize, "resources/loginBackground.png", TOPLEFT)
        IDTextBox = SimpleText("ID", (int(self.screenSize[0] * 1/ 4), int(self.screenSize[1] * 1 / 3)),
                               color = WHITE, bg_color= NAVY, anchor= TOPRIGHT, font=MyFont)

        IDInputBox = InLineTextBox(IDTextBox.topright + Sep(2 , 0), 300,
                                   BLACK, WHITE,anchor=TOPLEFT)

        IDWarningBox = SimpleText("ID must be at least 6 characters",IDInputBox.topleft + Sep(0, -1),
                                  color=RED,anchor=BOTTOMLEFT)
        PasswordWarningBox = SimpleText("Password must be at least 8 characters", IDInputBox.bottomleft + Sep(0, 2),
                                        color=RED,anchor=TOPLEFT)
        PasswordInputBox = InLinePassBox(PasswordWarningBox.bottomleft + Sep(0, 1),
                                         300, BLACK, WHITE, anchor= TOPLEFT)
        PasswordTextBox = SimpleText("PASSWORD", PasswordInputBox.topleft + Sep(-2,0),
                               color = WHITE, bg_color= NAVY, anchor= TOPRIGHT, font=MyFont)
        PasswordCheckWarningBox = SimpleText("Check password does not match", PasswordInputBox.bottomleft + Sep(0, 2),
                                             color=RED, anchor=TOPLEFT)
        PasswordCheckInputBox = InLinePassBox(PasswordCheckWarningBox.bottomleft + Sep(0, 1),
                                              300, BLACK, WHITE, anchor= TOPLEFT)
        PasswordCheckTextBox = SimpleText("PASSWORD CHECK", PasswordCheckInputBox.topleft + Sep(-2, 0),
                                          color=WHITE, bg_color=NAVY, anchor= TOPRIGHT, font=MyFont)
        NickNameWarningBox = SimpleText("Nickname must be at least 4 characters", PasswordCheckInputBox.bottomleft +Sep(0, 2),
                                        color=RED, anchor=TOPLEFT)
        NickNameInputBox = InLineTextBox(NickNameWarningBox.bottomleft + Sep(0, 1),
                                         300, BLACK, WHITE, anchor=TOPLEFT)
        NickNameTextBox = SimpleText("NICK NAME", NickNameInputBox.topleft + Sep(-2, 0),
                                          color=WHITE, bg_color=NAVY, anchor= TOPRIGHT, font=MyFont)

        ConfirmButton = Button(self.register,(int(self.screenSize[0]/ 2), int(self.screenSize[1] * 2 / 3)) + Sep(1, 0),(150,30),
                               "Register", color=BLACK, anchor=TOPRIGHT,takeArg=True, flags=BaseButton.THREADED_CALL| BaseButton.CALL_ON_PRESS)
        CancelButton = Button(self.cancel,ConfirmButton.topright + Sep(2,0),(150,30),
                              "Cancel", color=BLACK,takeArg=True, anchor=TOPLEFT)
        CancelButton.arg = StopRunning
        RegisterFailBox = SimpleText("Register failed",(10,10), RED, WHITE, anchor=TOPLEFT)
        RegisterFailBox.hide = True

        renderList = [background,IDTextBox,PasswordTextBox,PasswordCheckTextBox,NickNameTextBox,IDInputBox,PasswordInputBox,
                      PasswordCheckInputBox,NickNameInputBox,ConfirmButton,CancelButton,PasswordWarningBox,IDWarningBox,PasswordCheckWarningBox,
                      NickNameWarningBox, RegisterFailBox]

        feedEventList = [ConfirmButton, CancelButton]

        focus = FocusSelector(IDInputBox, PasswordInputBox, PasswordCheckInputBox, NickNameInputBox)
        focus.select(0)

        running = True
        while running:
            self.clock.tick(self.fpsLimit)
            mouse = pyg.mouse.get_pos()

            ConfirmButton.set_arg((IDInputBox.text,PasswordInputBox.text,NickNameInputBox.text))

            if len(IDInputBox.text) >= 6:
                IDWarningBox.hide = True
                IDcorrect = True
            else:
                IDWarningBox.hide = False
                IDcorrect = False

            if len(PasswordInputBox.text) >= 8:
                PasswordWarningBox.hide = True
                PasswordCorrect = True
            else:
                PasswordWarningBox.hide = False
                PasswordCorrect = False

            if PasswordInputBox.text == PasswordCheckInputBox.text:
                PasswordCheckWarningBox.hide = True
                PasswordCheckCorrect = True
            else:
                PasswordCheckWarningBox.hide = False
                PasswordCheckCorrect = False

            if len(NickNameInputBox.text) >= 4:
                NickNameWarningBox.hide = True
                NicknameCorrect = True
            else:
                NickNameWarningBox.hide = False
                NicknameCorrect = False

            if IDcorrect and PasswordCheckCorrect and PasswordCorrect and NicknameCorrect:
                ConfirmButton.isEnabled = True
            else:
                ConfirmButton.isEnabled = False

            for event in pyg.event.get():
                focus.selected().update(event)
                for item in feedEventList:
                    item.update(event)

                if event.type == QUIT:
                    self.stopGame()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if IDcorrect and PasswordCorrect and PasswordCheckCorrect and NicknameCorrect:
                            self.register(IDInputBox.text,PasswordInputBox.text,NickNameInputBox.text)

                    elif event.key == K_TAB:
                        if event.mod & KMOD_SHIFT:
                            focus.prev()
                        else:
                            focus.next()

                elif event.type == MOUSEBUTTONDOWN:
                    if mouse in IDInputBox:
                        focus.select(IDInputBox)
                    elif mouse in PasswordInputBox:
                        focus.select(PasswordInputBox)
                    elif mouse in PasswordCheckInputBox:
                        focus.select(PasswordCheckInputBox)
                    elif mouse in NickNameInputBox:
                        focus.select(NickNameInputBox)

                elif event.type == RegisterFailBoxShowEvent:
                    RegisterFailBox.hide = True
                elif event.type == StopRunning:
                    running = False

                if event.type == RegisterTimeoutEvent:
                    self.handler.receiveStop()

            while not self.handler.received.empty():
                message = self.handler.received.get()
                if message == RegisterSuccessful:
                    self.handler.receiveStop()
                    return True
                if message == RegisterFailed:
                    self.handler.receiveStop()
                    return False

            for item in renderList:
                item.render(self.screen)

            pyg.display.flip()
            pyg.display.update()


    def register(self, id, password, nickname):
        print(id,password,nickname)
        pyg.time.set_timer(RegisterTimeoutEvent,5000)
        data = ("REGISTER", id, password, nickname)
        self.handler.client.send(data)
        self.handler.receiveStart()


    def gameStartScreen(self):
        MyFont = Font(20,file= dirPath + r"/WHOOPASS.TTF")
        background = ImageBox((0,0), self.screenSize, "resources/loginBackground.png",anchor=TOPLEFT)
        """
        nicknameBox = SimpleText("Nickname : " + self.user.nickname, (20, 100),color=NAVY,bg_color=WHITE,font=MyFont,anchor=TOPLEFT)
        winRateBox = SimpleText("Win Rate : " + str(self.user.winRate), nicknameBox.bottomleft + Sep(0,3),
                                                    color = NAVY, bg_color=WHITE,font=MyFont, anchor=TOPLEFT)
        winBox = SimpleText("Games Won : " + str(self.user.wins), winRateBox.bottomleft + Sep(0, 3),
                            color = NAVY, bg_color=WHITE,font=MyFont,anchor=TOPLEFT)
        loseBox = SimpleText("Games Lost : " + str(self.user.loses), winBox.bottomleft + Sep(0,3),
                             color = NAVY, bg_color=WHITE,font=MyFont,anchor=TOPLEFT)
        gamesPlayed = SimpleText("Games Played : " + str(self.user.gamesPlayed),loseBox.bottomleft +Sep(0,3),
                                 color = NAVY, bg_color=WHITE,font=MyFont,anchor=TOPLEFT)
        doraemonRateBox = SimpleText("Doraemon Win Rate : " + str(self.user.doraemonWinRate), gamesPlayed.bottomleft + Sep(0, 3),
                                 color=NAVY, bg_color=WHITE, font=MyFont, anchor=TOPLEFT)
        doraemonWinBox = SimpleText("Doraemons Won : " + str(self.user.doraemonWins),doraemonRateBox.bottomleft +Sep(0,3),
                                 color = NAVY, bg_color=WHITE,font=MyFont,anchor=TOPLEFT)
        doraemonLoseBox = SimpleText("Doraemons Lost : " + str(self.user.doraemonLoses), doraemonWinBox.bottomleft + Sep(0, 3),
                                 color=NAVY, bg_color=WHITE, font=MyFont, anchor=TOPLEFT)
        doraemonPlayedBox = SimpleText("Doraemons Played: " + str(self.user.doraemonPlayed), doraemonLoseBox.bottomleft + Sep(0, 3),
                                 color=NAVY, bg_color=WHITE, font=MyFont, anchor=TOPLEFT)
        """

        gameReadyButton = Button(self.playerReady, (int(self.screenSize[0] / 2), int(self.screenSize[1] / 2)), (200,40), "Game Ready",
                                 color=NAVY)
        cancelButton = Button(self.cancel,gameReadyButton.bottomleft +Sep(0,3),(200,30),"Cancel",takeArg=True,anchor=TOPLEFT,color=NAVY,flags=BaseButton.CALL_ON_PRESS)
        cancelButton.set_arg(StopReady)
        ReadyCanceledBox = SimpleText("Ready Canceled",cancelButton.bottomleft + Sep(0,5),color=RED,font=MyFont,anchor=TOPLEFT)
        ReadyCanceledBox.hide = True
        renderList = [background,gameReadyButton,cancelButton,ReadyCanceledBox]

        running = True
        while running:
            self.clock.tick(self.fpsLimit)
            mouse = pyg.mouse.get_pos()

            for event in pyg.event.get():
                gameReadyButton.update(event)
                cancelButton.update(event)
                if event.type == QUIT:
                    self.stopGame()

                if event.type == StopReady:
                    self.handler.receiveStop()
                    data = ("READYSTOP")
                    self.handler.client.send(data)

            while not self.handler.received.empty():
                message = self.handler.received.get()
                if message == MatchingSuccessful:
                    self.handler.receiveStop()
                    return True

            for item in renderList:
                item.render(self.screen)

            pyg.display.flip()
            pyg.display.update()

    def playerReady(self):
        self.handler.receiveStart(num=1)
        data = ("READY")
        self.handler.client.send(data)

    def game(self):
        print("loading")
        self.handler.receiveStart()
        currentMap = None

        mapLoaded = False
        charactersLoaded = False

        loading = True
        while loading:
            while not self.handler.received.empty():
                message = self.handler.received.get()
                print(message)
                if message[0] == isMap:
                    print(message)
                    mapName = message[1]
                    #Map Put Here
                    if mapName == "simplemap":
                        currentMap = SimpleMap
                    print("Map loaded")
                    mapLoaded = True
                if message[0] == isCharacters:
                    print(message)
                    characterName = message[1]
                    if characterName == Zingu.name:
                        self.characterID = 0
                    elif characterName == Bisil.name:
                        self.characterID = 1
                    elif characterName == Toongtoong.name:
                        self.characterID = 2
                    elif characterName == Iseul.name:
                        self.characterID = 3
                    elif characterName == Doraemon.name:
                        self.characterID = 4
                    characterList = [Zingu,Bisil,Toongtoong,cIseul,Doraemon]
                    print("Character loaded")
                    charactersLoaded = True
                if message[0] == GameStart:
                    roomNum = message[1]
                    loading = False
            if mapLoaded and charactersLoaded:
                message = ("LOADCOMPLETE")
                self.handler.client.send(message)

        keys = {"right": False, "left": False, "up": False, "down": False, "bullet": False}
        direction = None
        running = True
        while running:
            self.clock.tick(self.fpsLimit)
            for event in pyg.event.get():
                if event.type == QUIT:
                    self.stopGame()
                if event.type == KEYDOWN:

                    if event.key == K_LEFT:
                        keys['left'] = True
                    elif event.key == K_RIGHT:
                        keys['right'] = True
                    elif event.key == K_UP:
                        keys['up'] = True
                    elif event.key == K_DOWN:
                        keys['down'] = True
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        keys['left'] = False
                    elif event.key == K_RIGHT:
                        keys['right'] = False
                    elif event.key == K_UP:
                        keys['up'] = False
                    elif event.key == K_DOWN:
                        keys['down'] = False

                if event.type == GameEndEvent:
                    self.characterID = None
                    self.handler.receiveStop()
                    return

            if keys['right'] == True and keys['left'] == False and keys['up'] == False and keys['down'] == False:
                direction = East
            elif keys['right'] == False and keys['left'] == True and keys['up'] == False and keys['down'] == False:
                direction = West
            elif keys['right'] == False and keys['left'] == False and keys['up'] == True and keys['down'] == False:
                direction = North
            elif keys['right'] == False and keys['left'] == False and keys['up'] == False and keys['down'] == True:
                direction = South
            elif keys['right'] == True and keys['left'] == False and keys['up'] == True and keys['down'] == False:
                direction = NE
            elif keys['right'] == True and keys['left'] == False and keys['up'] == False and keys['down'] == False:
                direction = SE
            elif keys['right'] == False and keys['left'] == True and keys['up'] == True and keys['down'] == False:
                direction = NW
            elif keys['right'] == False and keys['left'] == True and keys['up'] == False and keys['down'] == True:
                direction = SW
            else:
                direction = None



            while not self.handler.received.empty():
                message = self.handler.received.get()
                if message[0] == "MOVE":
                    if message[1].name == Zingu.name:
                        characterList[0] = message[1]
                    elif message[1].name == Bisil.name:
                        characterList[1] = message[1]
                    elif message[1].name == Toongtoong.name:
                        characterList[2] = message[1]
                    elif message[1].name == Iseul.name:
                        characterList[3] = message[1]
                    elif message[1].name == Doraemon.name:
                        characterList[4] = message[1]
                elif message[0] == GameEnd:
                    pyg.time.set_timer(GameEndEvent, GameEndTime)

            characterList[self.characterID].move(direction)
            for character in characterList:
                if character.name != Doraemon.name:
                    if character.rect.colliderect(characterList[4].rect):
                        character.isAlive = False
            currentMap.update(characterList[self.characterID])

            if direction != None:
                data = ("MOVE",roomNum,characterList[self.characterID])
                self.handler.client.send(data)

            currentMap.render(self.screen)
            for character in characterList:
                if character.isAlive == True:
                    character.render(self.screen)