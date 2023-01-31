import json
import os
from datetime import date

import pytest
from PyQt6 import QtCore
import View.window as v
from Const.const import TEST_FILES_DIR, PROTOCOLS_ACCEPTED_DIR, STATUS_ACCEPTED, PROTOCOLS_APPEAL_DIR, STATUS_IN_APPEAL, \
    STATUS_TO_ACCEPT
from Model.example_data import ProtocolResult, ProtocolResultList, print_results, create_appeal_from_protocol


@pytest.fixture
def app(qtbot):
    window = v.MainWindow()
    qtbot.addWidget(window)

    return window

# Model testing

def test_ProtocolResult_class_correct():
    filename = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    protocol = ProtocolResult(filename)
    assert protocol.id == "64"
    assert protocol.status == STATUS_TO_ACCEPT
    assert protocol.accepted_date == "---"
    assert protocol.received_date == "2023-01-28"

def test_ProtocolResult_class_exeption():
    filename = os.getcwd() + TEST_FILES_DIR + "\\incorrect_json.json"
    protocol = ProtocolResult(filename)
    assert protocol.id == "Niepoprawny format pliku"

def test_ProtocolResult_class_reload_data_correct():
    filename = os.getcwd() + TEST_FILES_DIR + "\\incorrect_json.json"
    protocol = ProtocolResult(filename)
    assert protocol.id == "Niepoprawny format pliku"
    protocol.path_to_file = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    protocol.reload_data()
    assert protocol.id == "64"
    assert protocol.status == STATUS_TO_ACCEPT
    assert protocol.accepted_date == "---"
    assert protocol.received_date == "2023-01-28"

def test_ProtocolResult_class_reload_data_exeption():
    filename = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    protocol = ProtocolResult(filename)
    assert protocol.id == "64"
    assert protocol.status == STATUS_TO_ACCEPT
    assert protocol.accepted_date == "---"
    assert protocol.received_date == "2023-01-28"
    protocol.path_to_file = os.getcwd() + TEST_FILES_DIR + "\\incorrect_json.json"
    protocol.reload_data()
    assert protocol.id == "Niepoprawny format pliku"

def test_ProtocolResultList_class_get_index_by_id():
    filename1 = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    filename2 = os.getcwd() + TEST_FILES_DIR + "\\incorrect_json.json"
    list = ProtocolResultList(99)
    list.list = [ProtocolResult(filename1), ProtocolResult(filename2)]
    assert list.get_index_by_id("64") == 0
    assert list.get_index_by_id("Niepoprawny format pliku") == 1

def test_ProtocolResultList_class_get_protocol_by_id():
    filename1 = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    filename2 = os.getcwd() + TEST_FILES_DIR + "\\incorrect_json.json"
    list = ProtocolResultList(99)
    list.list = [ProtocolResult(filename1), ProtocolResult(filename2)]
    assert list.get_protocol_by_id("64").id == "64"

def test_print_results():
    filename = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    protocol = ProtocolResult(filename)
    print_results(protocol)
    path = os.getcwd() + PROTOCOLS_ACCEPTED_DIR + "\\accepted_protocol_64.json"
    assert os.path.exists(path) == True
    f = open(path, encoding="utf-8")
    data = json.load(f)
    f.close()
    assert data["Podpis"] == ""
    assert data["Nr akceptacji"] == protocol.id
    assert data["Status protokołu"] == STATUS_ACCEPTED
    assert data["Data akceptacji"] == str(date.today())

def test_create_appeal_from_protocol():
    filename = os.getcwd() + TEST_FILES_DIR + "\\correct_json.json"
    protocol = ProtocolResult(filename)
    create_appeal_from_protocol("test", protocol)
    path = os.getcwd() + PROTOCOLS_APPEAL_DIR + "\\appeal_from_protocol_64.json"
    assert os.path.exists(path) == True

    f = open(protocol.path_to_file, encoding="utf-8")
    data = json.load(f)
    f.close()

    assert data["Status protokołu"] == STATUS_IN_APPEAL
    assert data["Nr odwołania"] == protocol.id

    f = open(protocol.path_to_file, "w", encoding="utf-8")
    data["Status protokołu"] = STATUS_TO_ACCEPT
    data["Nr odwołania"] = ""
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

    print("------------")
    print(path)


    f = open(path, "r", errors='ignore')
    data = json.load(f)
    f.close()

    assert data["Id Protokołu"] == protocol.id
    assert data["Treść Odwołania"] == "test"
    assert data["Data odowłania"] == str(date.today())
