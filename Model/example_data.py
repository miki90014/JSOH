import os
import secrets
import sys
from time import sleep, time
from datetime import date, datetime, time
from random import randrange, seed, randint


class ProtocolResult:
    def __init__(self):
        self.id = randint(1, 100)
        self.received_date = date.today()
        self.accepted_date = date.today()
        self.status = randint(0, 3)


class ProtocolResultList:
    def __init__(self, length):
        self.length = length
        self.list = []
        for i in range(length):
            self.list.append(ProtocolResult())

    def get_protocol_by_id(self, i):
        for protocol in self.list:
            if protocol.id == i:
                return protocol


def printResults(result):
    path = os.getcwd() + "\\Protocols"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The new directory is created!")
    filename = os.path.join("Protocols\\", secrets.token_hex(10)) + ".txt"
    f = open(filename, "x")
    f.write("Id Protokołu: {}".format(result.id))
    f.close()
    os.startfile(filename)


def send_accepted_protocol(filename):
    pass
