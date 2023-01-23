import os
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
        self.form = randint(1, 2)


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

    def get_index_by_id(self, i):
        index = -1
        for protocol in self.list:
            index += 1
            if protocol.id == i:
                return index


def print_results(result):
    path = os.getcwd() + "\\ProtocolsAccepted"
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print("The new directory is created!")
    filename = os.path.join("ProtocolsAccepted\\", "accepted_protocol")
    filename += "_" + str(result.id) + ".txt"
    f = open(filename, "x")
    f.write("Id Protokołu: {}".format(result.id))
    f.close()
    os.startfile(filename)

def create_appeal_from_protocol(text, result):
    path = os.getcwd() + "\\ProtocolsAppeal"
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print("The new directory is created!")
    filename = os.path.join("ProtocolsAppeal\\", "appeal_from_protocol")
    filename += "_" + str(result.id) + ".txt"
    f = open(filename, "x")
    f.write("ODWOŁANIE WYNIKU PROTOKOŁU\n")
    f.write("Id Protokołu: {}".format(result.id)+"\n")
    f.write("Treść Odwołania: {}".format(text)+"\n")
    f.write("\nData akceptacji: " + str(date.today()))
    f.close()

def send_accepted_protocol(filename):
    pass
