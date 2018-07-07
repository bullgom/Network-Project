import pickle
import multiprocessing
from Mastermind._mm_client import *
from Mastermind import *
from settings import *
import threading
from queue import Queue

class messageHandler():
    def __init__(self, ip, port):
        self.client = MastermindClientTCP(clientTimeoutConnect, clinetTimeoutRecieve)
        self.client.connect(ip, port)
        self._isReceiving = False
        self._received = Queue()
        self.receiveProcess = None

    @property
    def received(self):
        return self._received

    @property
    def isReceiving(self):
        return self._isReceiving

    @isReceiving.setter
    def isReceiving(self, value):
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean type")

    def _receive(self,num):
        for i in range(0,num):
            message = self.client.receive(blocking=True)
            self._received.put(message)

    def _receiveOnce(self):
        message = self.client.receive(blocking=True)
        self._received.put(message)

    def receiveStart(self, num=1):
        if(self.isReceiving):
            raise RuntimeError("Receive process is already running")
        self.isReceiving = True
        self.receiveProcess = threading.Thread(target=self._receive,args=(num,))
        self.receiveProcess.start()

    def receiveStop(self):
        self.isReceiving = False
        self.receiveProcess.join()