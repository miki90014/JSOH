import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette
from Model.example_data import ProtocolResult


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSOH")

        main_layout = QGridLayout()

        self.right_side_menu = QVBoxLayout()

        self.right_side_menu_button_list = [QPushButton('Przegląd zaplanowanych hospitacji'),
                                            QPushButton('Hospitacje'),
                                            QPushButton('Wgląd do wyników hospitacji'),
                                            QPushButton('Ocena pracowników'),
                                            QPushButton('Wypełnij protokół')]

        self.login_as_hospitowany()

        self.in_frame_layout = QGridLayout()

        for button in self.right_side_menu_button_list:
            self.right_side_menu.addWidget(button)

        login_list = QComboBox()
        login_list.addItems(["Hospitowany", 'Hospitujący', 'Dziekan'])
        login_list.currentIndexChanged.connect(self.on_login_list_change)

        frame = QFrame()
        frame.setStyleSheet("border: 1px solid black")

        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 10))

        main_layout.addLayout(self.right_side_menu, 1, 0)
        main_layout.addWidget(empty_widget, 0, 1)
        main_layout.addWidget(login_list, 0, 2)
        main_layout.addWidget(QPushButton('Powiadomienia'), 0, 3)
        main_layout.addWidget(QPushButton('Wyloguj się'), 0, 4)
        main_layout.addWidget(frame, 1, 1, 1, 4)
        main_layout.addLayout(self.in_frame_layout, 1, 1, 1, 4)

        self.setBaseSize(QSize(900, 450))

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

        # example of how connection will be working
        self.right_side_menu_button_list[2].clicked.connect(self.view_protocol_results)
        self.right_side_menu_button_list[1].clicked.connect(self.clear_in_frame_layout)
        self.right_side_menu_button_list[4].clicked.connect(self.fill_protocol)

    def fill_protocol(self):
        self.clear_in_frame_layout()
        for button in self.right_side_menu_button_list:
            button.hide()

        frame = QFrame()
        frame.setStyleSheet("border: 1px solid black")

        self.in_frame_layout.addWidget(frame, 0, 0, 4, 5)
        self.in_frame_layout.addWidget(QLabel("Ocena formalna zajęć:"), 0, 0)

        list_of_points = ['Punktualność zajęć', 'Sprawdzenie obecności studentów', 'Wyposażenie sali',
                          'Treść zgodna z kartą przedmiotu']

        radio_buttons = [QRadioButton('Tak'), QRadioButton('Nie'), QRadioButton('Nie dotyczy:')]
        radio_buttons_layout = QHBoxLayout()

        for button in radio_buttons:
            radio_buttons_layout.addWidget(button)

        for row, point in enumerate(list_of_points):
            self.in_frame_layout.addWidget(QLabel(point + ':'), row + 1, 0)
            self.in_frame_layout.addLayout(radio_buttons_layout, row + 1, 1, 1, 3)

    def login_as_hospitowany(self):
        for index, button in enumerate(self.right_side_menu_button_list):
            button.hide()
            if index == 2:
                button.show()

    def login_as_hospitujacy(self):
        for index, button in enumerate(self.right_side_menu_button_list):
            button.hide()
            if index in [0, 1, 2, 4]:
                button.show()

    def on_login_list_change(self, value):
        if value == 0:
            self.login_as_hospitowany()
        if value == 1:
            self.login_as_hospitujacy()
        if value == 2:
            self.right_side_menu_button_list[0].show()

    def clear_in_frame_layout(self):
        for i in reversed(range(self.in_frame_layout.count())):
            self.in_frame_layout.itemAt(i).widget().setParent(None)

    def view_protocol_results(self):
        self.clear_in_frame_layout()

        protocol_result_list = [ProtocolResult(), ProtocolResult()]

        frame = QFrame()
        frame.setStyleSheet("border: 1px solid black")

        self.in_frame_layout.addWidget(frame, 0, 0, 1, 5)
        self.in_frame_layout.addWidget(QLabel("nr Protokołu"), 0, 0)
        self.in_frame_layout.addWidget(QLabel("Data otrzymania"), 0, 1)
        self.in_frame_layout.addWidget(QLabel("Data wystawienia"), 0, 2)
        self.in_frame_layout.addWidget(QLabel("Status"), 0, 3)

        row = 1
        for result in protocol_result_list:
            self.in_frame_layout.addWidget(QLabel(str(result.id)), row, 0)
            self.in_frame_layout.addWidget(QLabel(str(result.received_date)), row, 1)
            self.in_frame_layout.addWidget(QLabel(str(result.accepted_date)), row, 2)
            match str(result.status):
                case '0':
                    self.in_frame_layout.addWidget(QLabel("Zaakceptowany"), row, 3)
                case '1':
                    self.in_frame_layout.addWidget(QLabel("Do zaakceptowania"), row, 3)
                case '2':
                    self.in_frame_layout.addWidget(QLabel("W trakcie odwołania"), row, 3)
                case '3':
                    self.in_frame_layout.addWidget(QLabel("Protokół zaakceptowany po odwołaniu"), row, 3)
            self.in_frame_layout.addWidget(QPushButton("Wgląd"), row, 4)
            row += 1
