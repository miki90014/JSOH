import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette


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

        right_side_menu = QVBoxLayout()

        right_side_menu.addWidget(QPushButton('Przegląd zaplanowanych hospitacji'))
        right_side_menu.addWidget(QPushButton('Wgląd do wyników hospitacji'))
        right_side_menu.addWidget(QPushButton('Hospitacje'))
        right_side_menu.addWidget(QPushButton('Ocena pracowników'))

        widget = QComboBox()
        widget.addItems(["Hospitowany", 'Hospitujący', 'Dziekan'])

        main_layout.addLayout(right_side_menu, 1, 0)
        main_layout.addWidget(QWidget(), 0, 1)
        main_layout.addWidget(widget, 0, 2)
        main_layout.addWidget(QPushButton('Powiadomienia'), 0, 3)
        main_layout.addWidget(QPushButton('Wyloguj się'), 0, 4)

        self.setFixedSize(QSize(900, 450))

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)


if __name__ == '__main__':
    window = MainWindow()
    window.show()

    app = QApplication([])

    app.exec()
