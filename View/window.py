import copy
import sys
from functools import partial

from PyQt6.QtCore import QSize, Qt, QDir
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette
from Model.example_data import ProtocolResult, ProtocolResultList, printResults, \
    send_accepted_protocol


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


def create_yes_no_radio_buttons():
    yes = QRadioButton('Tak')
    no = QRadioButton('Nie')
    not_included = QRadioButton('Nie dotyczy')
    group1 = QHBoxLayout()
    group = QGroupBox()
    group1.addWidget(yes)
    group1.addWidget(no)
    group1.addWidget(not_included)
    group.setLayout(group1)
    return group


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('JSOH')
        # for now
        self.protocol_result_list = ProtocolResultList(7)

        main_layout = QGridLayout()

        self.right_side_menu = QVBoxLayout()

        self.right_side_menu_button_list = [QPushButton('Przegląd zaplanowanych hospitacji'), QPushButton('Hospitacje'),
                                            QPushButton('Wgląd do wyników hospitacji'), QPushButton('Ocena pracowników')]

        self.in_frame_layout = QGridLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.inner = QFrame(self.scroll_area)
        self.inner.setLayout(self.in_frame_layout)

        self.scroll_area.setWidget(self.inner)

        for button in self.right_side_menu_button_list:
            self.right_side_menu.addWidget(button)

        login_list = QComboBox()
        login_list.addItems(['Hospitowany', 'Hospitujący', 'Dziekan'])
        login_list.currentIndexChanged.connect(self.on_login_list_change)

        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 10))

        main_layout.addLayout(self.right_side_menu, 1, 0)
        main_layout.addWidget(empty_widget, 0, 1)
        main_layout.addWidget(login_list, 0, 2)
        main_layout.addWidget(QPushButton('Powiadomienia'), 0, 3)
        main_layout.addWidget(QPushButton('Wyloguj się'), 0, 4)
        main_layout.addWidget(self.scroll_area, 1, 1, 1, 4)

        self.setBaseSize(QSize(900, 450))
        self.setFixedWidth(1000)
        self.setFixedHeight(300)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

        # example of how connection will be working
        self.right_side_menu_button_list[2].clicked.connect(self.view_protocol_results)
        self.right_side_menu_button_list[1].clicked.connect(self.view_protocols_to_fill)

    def on_login_list_change(self, value):
        self.hide_all_right_side_menu_button_list()
        if value == 0:
            self.right_side_menu_button_list[0].show()
            self.right_side_menu_button_list[1].show()
        if value == 1:
            self.right_side_menu_button_list[2].show()
        if value == 2:
            self.right_side_menu_button_list[3].show()

    def hide_all_right_side_menu_button_list(self):
        self.right_side_menu_button_list[0].hide()
        self.right_side_menu_button_list[1].hide()
        self.right_side_menu_button_list[2].hide()
        self.right_side_menu_button_list[3].hide()


    def clear_in_frame_layout(self):
        for i in reversed(range(self.in_frame_layout.count())):
            self.in_frame_layout.itemAt(i).widget().setParent(None)

    def view_protocol_results(self):
        self.clear_in_frame_layout()

        button_list = []

        frame = QFrame()
        frame.setStyleSheet('border: 1px solid black')

        self.in_frame_layout.addWidget(frame, 0, 0, 1, 5)
        self.in_frame_layout.addWidget(QLabel('nr Protokołu'), 0, 0)
        self.in_frame_layout.addWidget(QLabel('Data otrzymania'), 0, 1)
        self.in_frame_layout.addWidget(QLabel('Data wystawienia'), 0, 2)
        self.in_frame_layout.addWidget(QLabel('Status'), 0, 3)

        row = 1
        for i in range(self.protocol_result_list.length):
            button_list.append(QPushButton('Wgląd'))

        for result in self.protocol_result_list.list:
            self.in_frame_layout.addWidget(QLabel(str(result.id)), row, 0)
            self.in_frame_layout.addWidget(QLabel(str(result.received_date)), row, 1)
            self.in_frame_layout.addWidget(QLabel(str(result.accepted_date)), row, 2)
            match str(result.status):
                case '0':
                    self.in_frame_layout.addWidget(QLabel('Zaakceptowany'), row, 3)
                case '1':
                    self.in_frame_layout.addWidget(QLabel('Do zaakceptowania'), row, 3)
                case '2':
                    self.in_frame_layout.addWidget(QLabel('W trakcie odwołania'), row, 3)
                case '3':
                    self.in_frame_layout.addWidget(QLabel('Protokół zaakceptowany po odwołaniu'), row, 3)
            #button_list[row-1].clicked.connect(lambda: self.view_specific_protocol(result))
            button_list[row - 1].clicked.connect(partial(self.view_specific_protocol, result=result))
            self.in_frame_layout.addWidget(button_list[row-1], row, 4)
            row += 1


    def view_specific_protocol(self, result):
        self.clear_in_frame_layout()
        btn_back = QPushButton("Wróć do listy")
        btn_back.clicked.connect(self.view_protocol_results)

        self.in_frame_layout.addWidget(QLabel('Protokół hospitacji nr: '), 0, 0)
        self.in_frame_layout.addWidget(QLabel(str(result.id)), 0, 1)
        self.in_frame_layout.addWidget(btn_back, 0,2)

        if(result.status==1):
            answerResults = QPushButton('Odpowiedz na wyniki')
            answerResults.clicked.connect(lambda: self.answer_results(result))
            self.in_frame_layout.addWidget(answerResults, 0,3)
        else:
            alert = QMessageBox()
            alert.setText('Wyświetlany protokół zotsał zaakceptowany lub jest w trakcie odwołania. \nNie możesz podjąć żadnych akcji.')
            alert.exec()

    def answer_results(self, result):
        self.clear_in_frame_layout()
        btn_accept = QPushButton("Zaakceptuj")
        btn_cancellation = QPushButton("Napisz odwołanie")
        self.in_frame_layout.addWidget(QLabel("Czy chcesz zaakceptować wyniki?"), 0,0,2, 1)
        self.in_frame_layout.addWidget(btn_accept, 1,0)
        self.in_frame_layout.addWidget(btn_cancellation, 1, 1)
        btn_accept.clicked.connect(partial(self.accept_results, result=result))
        btn_cancellation.clicked.connect(partial(self.write_cancellation_results, result=result))

    def accept_results(self, result):
        self.clear_in_frame_layout()
        btn_print = QPushButton("Wydrukuj protokół")
        textEditor = QTextEdit()
        btn_upload = QPushButton("Załącz plik")
        btn_accept = QPushButton("Wyślij")
        self.in_frame_layout.addWidget(btn_print, 1, 0)
        self.in_frame_layout.addWidget(btn_upload, 1, 1)
        self.in_frame_layout.addWidget(textEditor, 0, 0, 1, 3)
        btn_print.clicked.connect(partial(printResults, result=result))
        btn_upload.clicked.connect(partial(self.get_text_file, textEditor=textEditor, btn_accept=btn_accept))

    def send_accepted_results(self, file_name):
        self.clear_in_frame_layout()
        send_accepted_protocol(file_name)

    def get_text_file(self, textEditor, btn_accept):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Txt File', r"Protocols",
                                                   "Text files (*.txt)")
        if(file_name.endswith('.txt')):
            with open(file_name, 'r') as f:
                data = f.read()
                textEditor.setPlainText(data)
                f.close()
            self.in_frame_layout.addWidget(btn_accept, 1, 2)
            btn_accept.clicked.connect(partial(self.send_accepted_results, file_name=file_name))
        else:
            pass

    def write_cancellation_results(self, result):
        self.clear_in_frame_layout()

    def view_protocols_to_fill(self):
        self.clear_in_frame_layout()

        button_list = []

        frame = QFrame()
        frame.setStyleSheet('border: 1px solid black')

        self.in_frame_layout.addWidget(frame, 0, 0, 1, 5)
        self.in_frame_layout.addWidget(QLabel('nr Protokołu'), 0, 0)
        self.in_frame_layout.addWidget(QLabel('Prowadzący'), 0, 1)
        self.in_frame_layout.addWidget(QLabel('Data hospitacji'), 0, 2)

        row = 1
        for i in range(self.protocol_result_list.length):
            button_list.append(QPushButton('Wypełnij'))

        for result in self.protocol_result_list.list:
            self.in_frame_layout.addWidget(QLabel(str(result.id)), row, 0)
            self.in_frame_layout.addWidget(QLabel("Jan Kowalski"), row, 1)
            self.in_frame_layout.addWidget(QLabel('2023-01-14'), row, 2)
            self.in_frame_layout.addWidget(QLabel('Do Wypełnienia'), row, 3)
            # button_list[row-1].clicked.connect(lambda: self.view_specific_protocol(result))
            button_list[row - 1].clicked.connect(lambda: self.fill_protocol(result))
            self.in_frame_layout.addWidget(button_list[row - 1], row, 4)
            row += 1

    def fill_protocol(self, result):
        self.clear_in_frame_layout()
        btn_back = QPushButton("Wróć do listy")
        btn_back.clicked.connect(self.view_protocols_to_fill)

        self.in_frame_layout.addWidget(QLabel('Protokół hospitacji nr: '), 0, 0)
        self.in_frame_layout.addWidget(QLabel(str(result.id)), 0, 1)
        self.in_frame_layout.addWidget(btn_back, 0, 2)

        # to be downloaded from database
        basic_info = [QLabel(f'Prawadzący zajęcia/Jednostka organizacyjna {"Jan Kowalski"}'),
                      QLabel(f'Nazwa kursu/kierunek studiów {"Projektowanie Oprogramowania"}'),
                      QLabel(f'Kod kursu {"KRK-054"}'),
                      QLabel(f'Forma dydaktyczna {""}'),
                      QLabel(f'Sposób realizacji {"tradycyjny"}'),
                      QLabel(f'Stopień i forma studiów {"I stopień"}'),
                      QLabel(f'Semestr {str(5)}'),
                      QLabel(f'Miejsce i termin zajęć {"Budynek D2, sala 152, wt 13:15-14:45"}'),
                      QLabel(f'Srodowisko realizacji zajęć {"Nie dotyczy"}')]

        row = 1
        for info in basic_info:
            self.in_frame_layout.addWidget(info, row, 0, 1, 2)
            row += 1

        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 25))

        self.in_frame_layout.addWidget(empty_widget, row, 0)
        row += 1

        self.in_frame_layout.addWidget(QLabel('Ocena formalna zajęć:'), row, 0, 1, 2)
        row += 1

        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 25))

        self.in_frame_layout.addWidget(empty_widget, row, 0)
        row += 1

        formal_mark = [QLabel('Punktualność zajęć: '),
                       QLabel('Sprawdzenie obecności studentów: '),
                       QLabel('Wyposażenie sali: '),
                       QLabel('Weryfikacja czy prowadzący jest widziany i słyszany: '),
                       QLabel('Treść zajęć zgodna z kartą przedmiotu: '),
                       QLabel('Prowadzący umożliwia dostęp do informacji przez środku komunikacji elektronicznej: ')]

        formal_mark_dict = {

        }

        delay_label = QLabel('Opóźnienie: ')

        for mark in formal_mark:
            self.in_frame_layout.addWidget(mark, row, 0)
            buttons = create_yes_no_radio_buttons()
            formal_mark_dict[mark.text()] = buttons
            self.in_frame_layout.addWidget(buttons, row, 1, 1, 2)
            row += 1
            if mark.text() == 'Punktualność zajęć: ':
                self.in_frame_layout.addWidget(delay_label, row, 0)
                delay = QTextEdit()
                formal_mark_dict[delay_label.text()] = delay
                self.in_frame_layout.addWidget(delay, row, 1, 1, 2)
                delay_label.hide()
                delay.hide()
                for widget in buttons.children():
                    if isinstance(widget, QRadioButton):
                        widget.clicked.connect(lambda : self.show_delay(buttons, delay_label, delay))
                row += 1

    def show_delay(self, buttons: QGroupBox, delay_label, delay):
        delay.hide()
        delay_label.hide()
        for button in buttons.children():
            if isinstance(button, QRadioButton):
                if button.text() == 'Tak':
                    button.setChecked(True)
                if button.isChecked() and button.text() == 'Tak':
                    print('ala')
                    delay.show()
                    delay_label.show()


    def view_specific_protocol(self, result):
        self.clear_in_frame_layout()
        btn_back = QPushButton("Wróć do listy")
        btn_back.clicked.connect(self.view_protocol_results)

        self.in_frame_layout.addWidget(QLabel('Protokół hospitacji nr: '), 0, 0)
        self.in_frame_layout.addWidget(QLabel(str(result.id)), 0, 1)
        self.in_frame_layout.addWidget(btn_back, 0,2)

        if(result.status==1):
            answerResults = QPushButton('Odpowiedz na wyniki')
            answerResults.clicked.connect(lambda: self.answer_results(result))
            self.in_frame_layout.addWidget(answerResults, 0,3)
        else:
            alert = QMessageBox()
            alert.setText('Wyświetlany protokół zotsał zaakceptowany lub jest w trakcie odwołania. \nNie możesz podjąć żadnych akcji.')
            alert.exec()

    def answer_results(self, result):
        self.clear_in_frame_layout()
        btn_accept = QPushButton("Zaakceptuj")
        btn_cancellation = QPushButton("Napisz odwołanie")
        self.in_frame_layout.addWidget(QLabel("Czy chcesz zaakceptować wyniki?"), 0,0,2, 1)
        self.in_frame_layout.addWidget(btn_accept, 1,0)
        self.in_frame_layout.addWidget(btn_cancellation, 1, 1)
        btn_accept.clicked.connect(partial(self.accept_results, result=result))
        btn_cancellation.clicked.connect(partial(self.write_cancellation_results, result=result))

    def accept_results(self, result):
        self.clear_in_frame_layout()
        btn_print = QPushButton("Wydrukuj protokół")
        textEditor = QTextEdit()
        btn_upload = QPushButton("Załącz plik")
        btn_accept = QPushButton("Wyślij")
        self.in_frame_layout.addWidget(btn_print, 1, 0)
        self.in_frame_layout.addWidget(btn_upload, 1, 1)
        self.in_frame_layout.addWidget(textEditor, 0, 0, 1, 3)
        btn_print.clicked.connect(partial(printResults, result=result))
        btn_upload.clicked.connect(partial(self.get_text_file, textEditor=textEditor, btn_accept=btn_accept))

    def send_accepted_results(self, file_name):
        self.clear_in_frame_layout()
        send_accepted_protocol(file_name)

    def get_text_file(self, textEditor, btn_accept):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Txt File', r"Protocols",
                                                   "Text files (*.txt)")
        if(file_name.endswith('.txt')):
            with open(file_name, 'r') as f:
                data = f.read()
                textEditor.setPlainText(data)
                f.close()
            self.in_frame_layout.addWidget(btn_accept, 1, 2)
            btn_accept.clicked.connect(partial(self.send_accepted_results, file_name=file_name))
        else:
            pass



    def write_cancellation_results(self, result):
        self.clear_in_frame_layout()


