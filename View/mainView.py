from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import *
from PyQt6 import QtWidgets

from Const.const import *
from Model.mainModel import UserData


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle('JSOH')
        self.dataUser = UserData('konto@pwr.edu.pl')
        print(self.dataUser.mail)

        self.UiComponents()
        layout = QVBoxLayout()
        self.setLayout(layout)
        button1 = QPushButton('Wgląd do wyników hospitacji')
        button1.setGeometry(200, 150, 100, 40)

        layout.addWidget(button1)

        self.show()

    def UiComponents(self):
        # creating a push button
        button1 = QPushButton("Wgląd do wyników hospitacji", self)
        button2 = QPushButton("btn2", self)

        btnMessage = QPushButton("Powiadomienia", self)
        btnLogOut = QPushButton("Wyloguj się", self)
        label = QLabel(self.dataUser.mail, self)

        # setting geometry of button
        button1.setGeometry(PADDING_LEFT, BTN_HEIGHT*2, BTN_WIDTH, BTN_HEIGHT)
        button2.setGeometry(PADDING_LEFT, BTN_HEIGHT*3+PADDING, BTN_WIDTH, BTN_HEIGHT)
        label.move(WIN_WIDTH-(350+2*PADDING), PADDING)
        btnMessage.move(WIN_WIDTH-(250+PADDING), PADDING)
        btnLogOut.move(WIN_WIDTH -150, PADDING)

        # adding action to a button
        #button.clicked.connect(self.clickme)

    def add(self):
        pass