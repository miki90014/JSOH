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

        self.right_side_menu_button_list = [QPushButton('Przegląd zaplanowanych hospitacji'), QPushButton('Hospitacje'),
                                            QPushButton('Wgląd do wyników hospitacji'), QPushButton('Ocena pracowników')]

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

        #example of how connection will be working
        self.right_side_menu_button_list[2].clicked.connect(self.view_protocol_results)
        self.right_side_menu_button_list[1].clicked.connect(self.clear_in_frame_layout)

    def on_login_list_change(self, value):
        print("combobox changed", value)
        if value == 1:
            self.right_side_menu_button_list[0].hide()
        if value == 0:
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
            self.in_frame_layout.addWidget(QLabel(str(result.id)))
            self.in_frame_layout.addWidget(QLabel(str(result.received_date)))
            self.in_frame_layout.addWidget(QLabel(str(result.accepted_date)))
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
