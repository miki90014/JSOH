import pytest
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
import View.window as v


@pytest.fixture
def app(qtbot):
    window = v.MainWindow()
    qtbot.addWidget(window)

    return window


def test_login(app: v.MainWindow):
    assert str(app.main_layout.itemAt(2).widget().currentText()) == 'Hospitujący'


def test_hospitacje_button(app: v.MainWindow, qtbot):
    qtbot.mouseClick(app.right_side_menu.itemAt(1).widget(), QtCore.Qt.MouseButton.LeftButton)
    assert app.inner.childAt(0, 0).text() == 'Wypełnij'
