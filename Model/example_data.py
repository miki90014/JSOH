import json
import os
import sys
from time import sleep, time
from datetime import date, datetime, time
from random import randrange, seed, randint


class Protocol:
    def __init__(self):
        self.id = randint(1, 100)
        self.received_date = date.today()
        self.accepted_date = date.today()
        self.status = randint(0, 3)
        self.form = randint(1, 2)


class ProtocolList:
    def __init__(self, length):
        self.length = length
        self.list = []
        for i in range(length):
            self.list.append(Protocol())



class ProtocolResult:
    def __init__(self, filename):
        self.path_to_file = filename

        f = open(filename, encoding="utf-8")

        data = json.load(f)

        self.id = data["Nr protokołu"]
        self.received_date = data["Data otrzymania"]
        self.status = data["Status protokołu"]
        self.accepted_date = data["Data akceptacji"]
        if data["Status protokołu"] == "Wypełniony":
            self.status = 'Do zaakceptowania'
        if data["Data akceptacji"] == "":
            self.accepted_date = '---'

        f.close()

    def reload_data(self):

        f = open(self.path_to_file, encoding="utf-8")

        data = json.load(f)

        self.id = data["Nr protokołu"]
        self.received_date = data["Data otrzymania"]
        self.status = data["Status protokołu"]
        self.accepted_date = data["Data akceptacji"]
        if data["Status protokołu"] == "Wypełniony":
            self.status = 'Do zaakceptowania'
        if data["Data akceptacji"] == "":
            self.accepted_date = '---'

        f.close()


class ProtocolResultList:
    def __init__(self, workerid):
        self.list = []
        for filename in os.listdir(os.getcwd() + "\\Protocols" + str(workerid)):
            self.list.append(ProtocolResult(os.getcwd() + "\\Protocols" + str(workerid)+"\\"+filename))

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
    with open(result.path_to_file, 'r', encoding="utf-8") as firstfile, open(filename, 'w', encoding="utf-8") as secondfile:
        for line in firstfile:
            secondfile.write(line)

    f = open(filename, encoding="utf-8")
    data = json.load(f)
    f.close()

    f = open(filename, "w", encoding="utf-8")
    string = {"Podpis":""}
    data["Nr akceptacji"] = result.id
    data["Status protokołu"] = "Zaakceptowany"
    data["Data akceptacji"] = str(date.today())
    data.update(string)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
    os.startfile(filename)

def create_appeal_from_protocol(text, result):

    f = open(result.path_to_file, encoding="utf-8")
    data = json.load(f)
    f.close()

    f = open(result.path_to_file, "w", encoding="utf-8")
    data["Status protokołu"] = "W trakcie odwołania"
    data["Nr odwołania"] = result.id
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

    path = os.getcwd() + "\\ProtocolsAppeal"
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print("The new directory is created!")
    filename = os.path.join("ProtocolsAppeal\\", "appeal_from_protocol")
    filename += "_" + str(result.id) + ".txt"
    f = open(filename, "w")
    f.write("ODWOŁANIE WYNIKU PROTOKOŁU\n")
    f.write("Id Protokołu: {}".format(result.id)+"\n")
    f.write("Treść Odwołania: {}".format(text)+"\n")
    f.write("\nData odowłania: " + str(date.today()))
    f.close()

def send_accepted_protocol(filename):
    pass
