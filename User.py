class User():
    def __init__(self, username, password, nickname):
        self._username = username
        self._password = password
        self._nickname = nickname
        self._winRate = None
        self._wins = 0
        self._loses = 0
        self._gamesPlayed = 0
        self._doraemonPlayed = 0
        self._doraemonWins = 0
        self._doraemonLoses = 0
        self._doraemonWinRate = 0
        self.currentIP = None

    def loginFrom(self, ip):
        self.currentIP = ip

    def userLogout(self):
        self.currentIP = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value , str):
            raise TypeError("Value must be a string type")
        elif len(value) < 6:
            raise ValueError("Value must be at least 6 characters")
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Value must be a string type")
        elif len(value) < 8:
            raise ValueError("Value must be at least 8 characters")
        self._password = value

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not isinstance(value, str):
            raise TypeError("Value must be string type")
        elif len(value) < 4:
            raise ValueError("Value must be at least 4 characters")

        self._nickname = value

    @property
    def winRate(self):
        return self._winRate

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._wins:
            raise ValueError("Value can only be incremented")
        self._wins = value
        self.winRate = self.wins / self.gamesPlayed



    @property
    def loses(self):
        return self._loses

    @loses.setter
    def loses(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._loses:
            raise ValueError("Value can only be incremented")
        self._loses = value

    @property
    def gamesPlayed(self):
        return self._gamesPlayed

    @gamesPlayed.setter
    def gamesPlayed(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._gamesPlayed:
            raise ValueError("Value can only be incremented")

        self._gamesPlayed = value

    @property
    def doraemonPlayed(self):
        return self._doraemonPlayed

    @doraemonPlayed.setter
    def doraemonPlayed(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._gamesPlayed:
            raise ValueError("Value can only be incremented")

        self._doraemonPlayed = value

    @property
    def doraemonWins(self):
        return self._doraemonWins

    @doraemonWins.setter
    def doraemonWins(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._wins:
            raise ValueError("Value can only be incremented")
        self._doraemonWins = value
        self._doraemonWinRate = self.doraemonWins / self.doraemonPlayed

    @property
    def doraemonLoses(self):
        return self._doraemonLoses

    @doraemonLoses.setter
    def doraemonLoses(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer type")
        elif value < self._loses:
            raise ValueError("Value can only be incremented")
        self._doraemonLoses = value

    @property
    def doraemonWinRate(self):
        return self._doraemonWinRate

    def gameWonDoraemon(self):
        self.doraemonPlayed += 1
        self.doraemonWins += 1

    def gameLostDoraemon(self):
        self.doraemonPlayed += 1
        self.doraemonLoses += 1



















