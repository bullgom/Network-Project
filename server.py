import socketserver
import threading
import random
import pickle
from time import gmtime, strftime
import copy

Game = []
que = []


def currentime():
    return int(strftime("%M", gmtime()))*60 + 3600*int(strftime("%H", gmtime())) + int(strftime("%S", gmtime()))


def packet_recv_tcp(socket):
    info = b""
    try:
        while len(info) < 17:
            got = socket.recv(17)
            if got == b"": return (None, False)
            info += got
    except:
        return (None, False)
    if info == b"": return (None, False)
    compression = int(info[0:1])
    length = int(info[1:])
    data_str = b""
    try:
        while len(data_str) < length:
            got = socket.recv(length)
            if got == b"": return (None, False)
            data_str += got
    except:
        return (None, False)
    if compression != 0:
        data_str = zlib.decompress(data_str)
    data = pickle.loads(data_str)
    return data, True


def packet_send(socket, data):  # E.g.: =(MM_TCP,None)
    compression = 0
    protocol_and_udpaddress = (1, None)
    if compression == False:
        compression = 0
    elif compression == None:
        compression = 0
    elif compression == True:
        compression = 9
    elif compression == MM_MAX:
        compression = 9

    data_to_send = str(compression).encode()  # length is now 1

    data_str = pickle.dumps(data)
    if compression != 0:
        data_str = zlib.compress(data_str, compre4ssion)

    length_str = str(len(data_str)).encode()
    data_to_send += (16 - len(length_str))*b" "
    data_to_send += length_str  # length is now 17
    data_to_send += data_str  # length is now 17+len(data_str)

    try:
        if protocol_and_udpaddress[0] == 1:
            socket.sendall(data_to_send)
        else:
            if protocol_and_udpaddress[1] == None:
                socket.sendall(data_to_send)
            else:
                socket.sendto(data_to_send, protocol_and_udpaddress[1])
        return True
    except:
        return False


gamecount = 0
Host = ''

Port = 7699

userlock = threading.Lock()

Roomlock = threading.Lock()

Loading = []

Loadinglock = threading.Lock()

users = {}
usersdb = {}


class UserManager:

    def __init__(self, conn, addr):

        self.conn = conn  # 클라이언트 자신의 소켓

        self.addr = addr  # 클라이언트 자신의 주소

    def addUser(self, username, pw):

        userlock.acquire()

        usersdb[username] = pw

        userlock.release()

    def login(self, msg):
        print('login start')
        _msg = msg
        userid = msg[1][0]
        pw = msg[1][1]
        if (userid in usersdb):
            if (pw != usersdb[userid]):
                packet_send(self.conn, "wrongusernameorpassword")
                return
        else:
            packet_send(self.conn, "wrongusernameorpassword")
            return
        userlock.acquire()
        users[userid] = (self.conn, self.addr)
        userlock.release()
        packet_send(self.conn, "loginsuccessful")

    def removeUser(self, username):

        if (username not in users):
            return

        userlock.acquire()

        del users[username]

        userlock.release()

    def getUsers(self):

        print(users)

        return users

    def testusers(self):

        print(usersdb)

    def registerUsername(self, msg_):
        msg_ = msg_[1]
        userid = msg_[0]
        userpw = msg_[1]
        if userid in usersdb:
            packet_send(self.conn, "registerfailed")
            return
        self.addUser(userid, userpw)
        packet_send(self.conn, "registersuccessful")

    def Readycomplete(self):
        global gamecount
        DO = []
        for x in que:
            DO.append(x)
        que[0:] = []
        Loading.append([DO, 0])
        print(Loading)
        Game.append([DO, 0, []])
        print(Game)
        gamecount += 1
        for x in Game[gamecount - 1][0]:
            packet_send(x[0], "matchingsuccessful")

    def loadingcomplete(self):
        for x in Loading:
            if (self.conn in x[0][0]):
                print(x[1])
                if (x[1] != 4):
                    x[1] += 1
                    print(Loading)
                    break
                else:
                    for y in x[0]:
                        packet_send(y[0], "gamestart")
                    for x in Game:
                        if (self.conn in x[0][0]):
                            x[1] = currentime()

    def Update(self):
        gameindex = 0
        gamecharac = 0
        print(Game[gameindex][1])
        print(currentime())
        if (Game[gameindex][1] + 80 < currentime()):  # 시간초 다됨
            for x in Game[gameindex][0]:
                packet_send(x[0], "Timeout")
        else:
            pass

    def Ready(self):
        if (len(que) == 4):
            print(que)
            self.Readycomplete()
        else:
            que.append((self.conn, self.addr))
            print(que)

    def ReadyCancel(self):
        for x in range(0, len(que)):
            if (self.conn == que[x][0]):
                del que[x]
        print(que)

    def detectgame(self):
        print(Game)

    def detectque(self):
        print(que)


def login_mode(userman, msg):
    conn = userman.conn

    addr = userman.addr
    if ("Update" in msg[0]):
        userman.Update()
    if ("detectgame" in msg[0]):
        userman.detectgame()
    if ("" in msg[0]):
        userman.Update()
    if ("detectque" in msg[0]):
        userman.detectque()
    if ("READY" in msg[0]):
        userman.Ready()
    if ("Loadingcomplete" in msg[0]):
        userman.loadingcomplete()
    if ("LOGIN" in msg[0]):
        userman.login(msg[0])

    if ("REGISTER" in msg[0]):
        userman.registerUsername(msg[0])

    if ("testusers" in msg[0]):
        userman.testusers()

    if ("getIUsers" in msg[0]):
        userman.getUsers()
    if ("ReadyCancel" in msg[0]):
        userman.ReadyCancel()


def game_mode(msg):
    pass


class ConnHandler(socketserver.BaseRequestHandler):  # only receive message

    def handle(self):  # 클라이언트가 접속시 클라이언트 주소 출력

        mode = 1

        userman = UserManager(self.request, self.client_address[0])
        print('[%s] 연결됨'%self.client_address[0])

        try:

            print('wait user signal')
            while (True):
                msg = packet_recv_tcp(self.request)
                login_mode(userman, msg)
        except Exception as e:

            print(e)

        print('[%s] 접속종료'%self.client_address[0])

        try:

            userman.removeUser(username)

        except:

            print("quit before register")


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ 게임 서버를 시작합니다.')

    print('+++ 게임 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:

        server = ChatingServer((Host, Port), ConnHandler)

        server.serve_forever()

    except KeyboardInterrupt:

        print('— 채팅 서버를 종료합니다.')

        server.shutdown()

        server.server_close()


runServer()