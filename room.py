class Room:
    since = 0

    def __init__(self, host, title):
        self.title = title
        self.numPeople = None
        self.isSelectable = False
        self.since += 1
        self.id = self.since
        self.participantArray = []
        self.host = host
        self.readyArray = []
        self.volunteerArray = []
        self.chatBox = chatManager()
        self.networkManager = NetworkManager()
        self.map = Map()

    def ready(self, user):
        self.readyArray.append(user)

    def gameStart(self):
        Ingame()
        del self

    def participate(self, user):
        self.valunteerArray.append(user)

    def newUser(self, user):
        self.numPeople += 1
        self.participantArray.append(user)

    def exit(self, user):
        self.readyArray.remove(user)
        if user in self.voluteerArray:
            self.volunteerArray.remove(user)
