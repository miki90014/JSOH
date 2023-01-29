import json
import os
import sys
from time import sleep, time
from datetime import date, datetime, time
from random import randrange, seed, randint
from PyQt6.QtWidgets import *


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
        for _ in range(length):
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


def avg(number_list):
    number_list = [i for i in number_list if i != 0]
    average = sum(number_list)/len(number_list)
    return round(average, 2)


def sorter(item):
    sort_by = item[1]['Ocena merytoryczna']['Ocena końcowa']
    if sort_by == 'negatywna':
        return 1
    elif sort_by == 'dostateczna':
        return 2
    elif sort_by == 'dobra':
        return 3
    elif sort_by == 'bardzo dobra':
        return 4
    else:
        return 5


def save_protocol_to_file(result, basic_info, formal_mark, substansive_mark):
    folder = os.getcwd() + '\\Protocols'
    if not os.path.exists(folder):
        os.mkdir(folder)

    json_string = {
        'Nr protokołu': f'{result["Nr protokołu"]}',
        'Nr hospitacji': f'{result["Nr hospitacji"]}',
    }

    file = folder + '\\protocol_' + result["Nr protokołu"] + '.json'
    for label, value in basic_info.items():
        json_string[label] = value

    json_string['Ocena formalna'] = {

    }
    for key, value in formal_mark.items():
        key = key.split(':')[0]

        for widget in value.children():
            if isinstance(widget, QRadioButton):
                if widget.isChecked():
                    json_string['Ocena formalna'][key] = widget.text()
        if isinstance(value, QTextEdit):
            json_string['Ocena formalna'][key] = value.toPlainText()

    json_string['Ocena merytoryczna'] = {

    }
    for key, value in substansive_mark.items():
        key = key.split(':')[0]

        for widget in value.children():
            if isinstance(widget, QRadioButton):
                if widget.isChecked():
                    json_string['Ocena merytoryczna'][key] = widget.text()

        if isinstance(value, QTextEdit):
            json_string['Ocena merytoryczna'][key] = value.toPlainText()

        if isinstance(value, QLabel):
            json_string['Ocena merytoryczna'][key] = value.text()

    json_string['Status protokołu'] = 'Wypełniony'
    json_string['Data otrzymania'] = datetime.today().strftime('%Y-%m-%d')
    json_string['Data akceptacji'] = ''

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(json_string, f, ensure_ascii=False, indent=4)


def filter_list(protocols_to_filter: dict, number: str):
    """

    :param protocols_to_filter:
    :param number: semester number to be used as filter key
    :return: a new dict of protocols where field semester is equal to number
    """
    filtered = {key: value for key, value in protocols_to_filter.items() if value['Semestr'] == number}
    return filtered


def sort_protocols_list(order: str, order_by: str, protocols_to_sort: dict, number: str):
    """

    :param order: order of sorting
    :param order_by:
    :param protocols_to_sort:
    :param number: semester number to be used as filter key

        if no order is specified:
            :return: protocols_to_sort without any changes
        else:
            :return: protocols sorted and filtered according to parameters
    """
    if order == 'Brak':
        return protocols_to_sort
    if number != 'Brak':
        protocols_to_sort = filter_list(protocols_to_sort, number)
    order = False if order == 'Rosnąco' else True
    if order_by == 'nr Protokołu':
        sorted_protocols = sorted(protocols_to_sort.items(),
                                  key=lambda item: item[1]
                                  ['Nr protokołu'],
                                  reverse=order)
    elif order_by == 'Prowadzący':
        sorted_protocols = sorted(protocols_to_sort.items(),
                                  key=lambda item: item[1]
                                  ['Prowadzący zajęcia/Jednostka organizacyjna'],
                                  reverse=order)
    elif order_by == 'Data hospitacji':
        sorted_protocols = sorted(protocols_to_sort.items(),
                                  key=lambda item: item[1]
                                  ['Data otrzymania'],
                                  reverse=order)
    elif order_by == 'Ocena pracownika':
        sorted_protocols = sorted(protocols_to_sort.items(),
                                  key=lambda item: sorter(item),
                                  reverse=order)
    else:
        sorted_protocols = {

        }
    sorted_protocols = dict(sorted_protocols)
    return sorted_protocols


def load_unfilled_protocols():
    protocols = []
    path = f'{os.getcwd()}\\Protocols_unfilled'
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                protocols.append(os.path.join(r, file))

    protocols_in_dir = {

    }

    for protocol in protocols:
        with open(protocol, 'r', encoding='utf-8') as file:
            protocol_number = os.path.basename(protocol).split('_')[1].split('.')[0]
            protocols_in_dir[protocol_number] = json.load(file)
    return protocols_in_dir
