import json
import os
from datetime import date

import pytest
from PyQt6 import QtCore
import View.window as v

@pytest.fixture
def app(qtbot):
    window = v.MainWindow()
    qtbot.addWidget(window)

    return window

def test_read_data(app: v.MainWindow, qtbot):
    filepath = "TestData/"
    data = app.read_data(filepath)
    item = data[0][0]
    assert item["Data ostatniej hospitacji"] == "2022-01-28"
    assert item["Hospitowany"] == "Jan Kowalski"
    assert item["Nazwa kursu"] == "Bazy danych"
    assert item["Kod grupy"] == "K01-35k"

def test_add_to_schedule(app: v.MainWindow):
    file_path = "TestData/test_schedule.json"
    folder_path = "TestData/"
    new_employee = {"Data ostatniej hospitacji":"2022-02-12","Imie":"Alan", "Nazwisko":"Byk"}
    new_classes = {"Nazwa":"Projektowanie oprogramowania","Kod grupy":"K00-12d"}
    app.add_to_schedule(new_employee, new_classes, file_path)
    data = app.read_data(folder_path)
    assert data[0][-1] == {"Data ostatniej hospitacji": "2022-02-12", "Hospitowany": "Alan Byk", "Nazwa kursu": "Projektowanie oprogramowania", "Kod grupy": "K00-12d"}

def test_remove_from_schedule(app:v.MainWindow):
    file_path = "TestData/test_schedule.json"
    folder_path = "TestData/"
    data_to_remove = {"Data ostatniej hospitacji": "2022-02-12", "Hospitowany": "Alan Byk", "Nazwa kursu": "Projektowanie oprogramowania", "Kod grupy": "K00-12d"}
    app.remove_from_schedule(data_to_remove, file_path)
    data = app.read_data(folder_path)
    assert data[0][-1] != {"Data ostatniej hospitacji": "2022-02-12", "Hospitowany": "Alan Byk", "Nazwa kursu": "Projektowanie oprogramowania", "Kod grupy": "K00-12d"}

def test_add_to_schedule_exception(app: v.MainWindow):
    file_path = "TestData/test_schedule.json"
    folder_path = "TestData/"
    new_employee = {"Data ostatniej hospitacji":"2022-02-12","Imie":"Anna", "Nazwisko":"Nowak"}
    new_classes = {"Nazwa":"Projektowanie oprogramowania","Kod grupy":"K00-12c"}
    app.add_to_schedule(new_employee, new_classes, file_path)
    data = app.read_data(folder_path)
    assert data[0][-1] == {"Data ostatniej hospitacji": "2022-02-12", "Hospitowany": "Damian Byk", "Nazwa kursu": "Projektowanie oprogramowania", "Kod grupy": "K00-12d"}