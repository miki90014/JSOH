from View import window as v
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])

    window = v.MainWindow()
    window.show()

    app.exec()
