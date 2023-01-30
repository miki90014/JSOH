import json

import pytest
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
import View.window as v
from Model.example_data import avg, sorter


@pytest.fixture
def app(qtbot):
    window = v.MainWindow()
    qtbot.addWidget(window)

    return window


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 1, 1, 1], 1),
        ([], 0),
        ([5.5, 5.5, 0, 5.5, 0], 5.5),
        ([0, 0, 0, 0, 0], 0),
        ([1, 2, 3], 2),
        ([5.5, 5, 4, 3.5], 4.5)
    ]
)
def test_avg(numbers, expected):
    assert avg(numbers) == expected


def file():
    with open('Protocols/protocol_01.json', encoding='utf-8') as f:
        return json.load(f)


@pytest.mark.parametrize(
    "mark, expected",
    [
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'wzorowa'
            }}], 5),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'dostateczna'
            }}], 2),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': 'inna'
            }}], 0),
        ([1, {
            'Ocena merytoryczna': {
                'Ocena końcowa': ''
            }}], 0),
    ]
)
def test_sorter(mark, expected):
    assert sorter(mark) == expected
