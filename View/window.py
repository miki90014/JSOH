import copy
import os
import sys
import json
from datetime import date, datetime
from functools import partial

from PyQt6.QtCore import QSize, Qt, QDir
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette
from Model.example_data import ProtocolResult, ProtocolResultList, print_results, \
    send_accepted_protocol, create_appeal_from_protocol


def create_yes_no_radio_buttons():
    yes = QRadioButton('Tak')
    no = QRadioButton('Nie')
    not_included = QRadioButton('Nie dotyczy')

    not_included.setChecked(True)

    group1 = QHBoxLayout()
    group = QGroupBox()
    group1.addWidget(yes)
    group1.addWidget(no)
    group1.addWidget(not_included)
    group.setLayout(group1)
    return group


def create_enum_buttons():
    six = QRadioButton('5.5')
    five = QRadioButton('5')
    four = QRadioButton('4')
    three = QRadioButton('3')
    two = QRadioButton('2')
    zero = QRadioButton('0')

    zero.setChecked(True)

    group1 = QHBoxLayout()
    group = QGroupBox()
    group1.addWidget(six)
    group1.addWidget(five)
    group1.addWidget(four)
    group1.addWidget(three)
    group1.addWidget(two)
    group1.addWidget(zero)
    group.setLayout(group1)
    return group


def show_fields(buttons: QGroupBox, field_label, field, reverse=False):
    field.hide()
    field_label.hide()
    expected = 'Tak' if not reverse else 'Nie'
    for button in buttons.children():
        if isinstance(button, QRadioButton):
            if button.isChecked() and button.text() == expected:
                field.show()
                field_label.show()


def calculate_avg(substansive_mark_dict, label):
    value = 0
    total = len(substansive_mark_dict) - 3
    for buttons in substansive_mark_dict.values():
        for child in buttons.children():
            if isinstance(child, QRadioButton):
                value += float(child.text()) if child.isChecked() else 0
                total -= 1 if child.text() == '0' and child.isChecked() else 0
    label.setText(str(round(value/total, 2)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('JSOH')
        # for now
        self.protocol_result_list = ProtocolResultList(20)

        self.main_layout = QGridLayout()

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
        login_list.addItems(['Hospitujący', 'Hospitowany', 'Dziekan'])
        login_list.currentIndexChanged.connect(self.on_login_list_change)

        frame = QFrame()
        frame.setStyleSheet('border: 1px solid black')

        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 10))

        self.main_layout.addLayout(self.right_side_menu, 1, 0)
        self.main_layout.addWidget(empty_widget, 0, 1)
        self.main_layout.addWidget(login_list, 0, 2)
        self.main_layout.addWidget(QPushButton('Powiadomienia'), 0, 3)
        self.main_layout.addWidget(QPushButton('Wyloguj się'), 0, 4)
        self.main_layout.addWidget(frame, 1, 1, 1, 4)
        self.main_layout.addWidget(self.scroll_area, 1, 1, 1, 4)

        empty = QWidget()
        empty.setFixedSize(QSize(100, 50))
        self.main_layout.addWidget(empty, 2, 0)

        self.setBaseSize(QSize(900, 450))
        self.setFixedWidth(1150)
        self.setFixedHeight(450)

        widget = QWidget()
        widget.setLayout(self.main_layout)

        self.setCentralWidget(widget)

        self.right_side_menu_button_list[1].clicked.connect(self.view_protocols_to_fill)
        self.right_side_menu_button_list[2].clicked.connect(self.view_protocol_results)
        self.right_side_menu_button_list[3].clicked.connect(self.view_and_sort_protocols)

        self.hide_all_right_side_menu_button_list()
        self.right_side_menu_button_list[0].show()
        self.right_side_menu_button_list[1].show()

    def on_login_list_change(self, value):
        self.clear_in_frame_layout()
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
        btn_print.clicked.connect(partial(print_results, result=result))
        btn_upload.clicked.connect(partial(self.get_text_file, textEditor=textEditor, btn_accept=btn_accept))

    def send_accepted_results(self, file_name):
        self.clear_in_frame_layout()
        send_accepted_protocol(file_name)

    def get_text_file(self, textEditor, btn_accept):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Txt File', r"Protocols",
                                                   "Text files (*.txt)")
        if file_name.endswith('.txt'):
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

        self.in_frame_layout.addWidget(frame, 0, 0, 1, 6)
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
            self.in_frame_layout.addWidget(QLabel('Wykład' if result.form == 1 else 'Inny'), row, 4)
            # button_list[row-1].clicked.connect(lambda: self.view_specific_protocol(result))
            button_list[row - 1].clicked.connect(partial(self.fill_protocol, result=result))
            self.in_frame_layout.addWidget(button_list[row - 1], row, 5)
            row += 1

    def stop_filling_protocol(self):
        alert = QMessageBox()
        alert.setText('Anulowano wypełnianie protokołu')
        alert.exec()
        self.view_protocols_to_fill()

    def save_protocol(self, result, basic_info, formal_mark, substansive_mark):
        folder = os.getcwd() + '\\Protocols'
        if not os.path.exists(folder):
            os.mkdir(folder)

        json_string = {
            'Nr protokołu': f'{result.id}',
            'Nr hospitacji': f'unknown',
        }

        file = folder + '\\protocol_' + str(result.id) + '.json'

        with open(file, 'w', encoding="utf-8") as f:
            # f.write('Protokół hospitacji nr: ' + str(result.id) + '\n')
            # f.writelines([label + ' ' + value + '\n' for label, value in basic_info.items()])
            for label, value in basic_info.items():
                json_string[label] = value

            # f.write('\nOcena formalna zajęć: \n\n')
            json_string['Ocena formalna'] = {

            }
            for key, value in formal_mark.items():
                key = key.split(':')[0]
                # f.write(key)

                for widget in value.children():
                    if isinstance(widget, QRadioButton):
                        if widget.isChecked():
                            # f.write(widget.text() + '\n')
                            json_string['Ocena formalna'][key] = widget.text()
                if isinstance(value, QTextEdit):
                    # f.write(value.toPlainText() + '\n')
                    json_string['Ocena formalna'][key] = value.toPlainText()

            # f.write('\nOcena merytoryczna zajęć: \n\n')

            json_string['Ocena merytoryczna'] = {

            }
            for key, value in substansive_mark.items():
                key = key.split(':')[0]
                # f.write(key)

                for widget in value.children():
                    if isinstance(widget, QRadioButton):
                        if widget.isChecked():
                            # f.write(widget.text() + '\n')
                            json_string['Ocena merytoryczna'][key] = widget.text()

                if isinstance(value, QTextEdit):
                    # f.write(value.toPlainText() + '\n')
                    json_string['Ocena merytoryczna'][key] = value.toPlainText()

                if isinstance(value, QLabel):
                    # f.write(value.text() + '\n')
                    json_string['Ocena merytoryczna'][key] = value.text()

        json_string['Status protokołu'] = 'Wypełniony'
        json_string['Data otrzymania'] = datetime.today().strftime('%Y-%m-%d')
        json_string['Nr akceptacji'] = ''
        json_string['Nr odwołania'] = ''

        alert = QMessageBox()
        alert.setText('Zapisano protokół')

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(json_string, f, ensure_ascii=False, indent=4)

        alert.exec()
        self.view_protocols_to_fill()

    def fill_protocol(self, result):
        self.clear_in_frame_layout()

        btn_back = QPushButton("Anuluj")
        btn_back.clicked.connect(self.stop_filling_protocol)

        btn_accept = QPushButton("Zaakceptuj protokół")
        btn_accept.clicked.connect(lambda: self.save_protocol(result, basic_info_for_save, formal_mark_dict,
                                                              substansive_mark_dict))

        self.in_frame_layout.addWidget(QLabel('Protokół hospitacji nr: '), 0, 0)
        self.in_frame_layout.addWidget(QLabel(str(result.id)), 0, 1)

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

        basic_info_for_save = {
            'Prawadzący zajęcia/Jednostka organizacyjna': "Jan Kowalski",
            'Nazwa kursu/kierunek studiów': "Projektowanie Oprogramowania",
            'Kod kursu': "KRK-054",
            'Forma dydaktyczna': "",
            'Sposób realizacji': "tradycyjny",
            'Stopień i forma studiów': "I stopień",
            'Semestr': str(5),
            'Miejsce i termin zajęć': "Budynek D2, sala 152, wt 13:15-14:45",
            'Srodowisko realizacji zajęć': "Nie dotyczy"
        }

        row = 1
        for info in basic_info:
            self.in_frame_layout.addWidget(info, row, 0, 1, 2)
            row += 1

        row = self.add_empty_widget(row)

        self.in_frame_layout.addWidget(QLabel('Ocena formalna zajęć:'), row, 0, 1, 2)
        row += 1

        row = self.add_empty_widget(row)

        formal_mark_template = ['Punktualność zajęć: ', 'Sprawdzenie obecności studentów: ', 'Wyposażenie sali: ',
                                'Weryfikacja czy prowadzący jest widziany i słyszany: ',
                                'Treść zajęć zgodna z kartą przedmiotu: ',
                                'Prowadzący umożliwia dostęp do informacji przez środku komunikacji elektronicznej: ']

        formal_mark = []

        for mark in formal_mark_template:
            formal_mark.append(QLabel(mark))

        formal_mark_dict = {

        }

        delay_label = QLabel('Opóźnienie: ')

        present_label = QLabel('Liczba obecnych: ')

        eq_label = QLabel('Dlaczego sala jest niewyposażona: ')

        for mark in formal_mark:
            self.in_frame_layout.addWidget(mark, row, 0)
            buttons = create_yes_no_radio_buttons()
            formal_mark_dict[mark.text()] = buttons
            self.in_frame_layout.addWidget(buttons, row, 1, 1, 2)
            row += 1
            if mark.text() == 'Punktualność zajęć: ':
                buttons_delay = buttons
                self.in_frame_layout.addWidget(delay_label, row, 0)
                delay = QTextEdit()
                formal_mark_dict[delay_label.text()] = delay
                self.in_frame_layout.addWidget(delay, row, 1, 1, 2)
                delay_label.hide()
                delay.hide()
                for widget in buttons_delay.children():
                    if isinstance(widget, QRadioButton):
                        widget.clicked.connect(lambda : show_fields(buttons_delay, delay_label, delay))
                row += 1

            if mark.text() == 'Sprawdzenie obecności studentów: ':
                buttons_present = buttons
                self.in_frame_layout.addWidget(present_label, row, 0)
                present = QTextEdit()
                formal_mark_dict[present_label.text()] = present
                self.in_frame_layout.addWidget(present, row, 1, 1, 2)
                present_label.hide()
                present.hide()
                for widget in buttons_present.children():
                    if isinstance(widget, QRadioButton):
                        widget.clicked.connect(lambda: show_fields(buttons_present, present_label, present))
                row += 1

            if mark.text() == 'Wyposażenie sali: ':
                buttons_eq = buttons
                self.in_frame_layout.addWidget(eq_label, row, 0)
                eq = QTextEdit()
                formal_mark_dict[eq_label.text()] = eq
                self.in_frame_layout.addWidget(eq, row, 1, 1, 2)
                eq_label.hide()
                eq.hide()
                for widget in buttons_eq.children():
                    if isinstance(widget, QRadioButton):
                        widget.clicked.connect(lambda: show_fields(buttons_eq, eq_label, eq, True))
                row += 1

        formal_mark_other = QTextEdit()

        self.in_frame_layout.addWidget(QLabel('Inne uwagi: '), row, 0, 1, 2)
        self.in_frame_layout.addWidget(formal_mark_other, row, 1, 1, 2)
        row += 1

        formal_mark_dict['Inne uwagi: '] = formal_mark_other

        row = self.add_empty_widget(row)

        self.in_frame_layout.addWidget(QLabel('Ocena merytoryczna ogólna:'), row, 0, 1, 2)
        row += 1

        row = self.add_empty_widget(row)

        substansive_mark_template = ['Przedstawia temat', 'Wyjaśnia zagadnienia', 'Realizuje zajęcia z zaangażowaniem',
                                     'Inspiruje studentów do samodzielnego myślenia', 'Odpowiada na pytania studentów',
                                     'Stosuje środki dydaktyczne', 'Posługuje się poprawnym językiem',
                                     'Panuje nad dynamiką grupy', 'Tworzy pozytywną atmosferę podczas zajęć',
                                     'Sprawnie posługuje się technicznymi środkami przekazu wiedzy']

        # jeżeli wykład to:
        if result.form == 1:
            substansive_mark_template.extend(['Przekazuje aktualną wiedzę',
                                              'Przedstawia materiał w sposób zorganizowany i uporządkowany',
                                              'Wykazuje się umiejętnościami nauczania',
                                              'Poprawny dobór przykładów',
                                              'Odpowiednie tempo prowadzonych zajęć'])
        else:
            substansive_mark_template.extend(['Przygotowanie merytoryczne do danej formy zajęć',
                                              'Określenie zadań dla studentów',
                                              'Rozplanowanie zajęć w czasie',
                                              'Kontrola umiejętności zdobytych podczas zajęć',
                                              'Prowadzenie dokumentacji zajęć'])

        substansive_mark = []

        for mark in substansive_mark_template:
            mark += ': '
            substansive_mark.append(QLabel(mark))

        substansive_mark_dict = {

        }

        avarage_mark = QLabel('0')

        for mark in substansive_mark:
            self.in_frame_layout.addWidget(mark, row, 0)
            buttons = create_enum_buttons()
            substansive_mark_dict[mark.text()] = buttons
            self.in_frame_layout.addWidget(buttons, row, 1, 1, 2)
            for widget in buttons.children():
                if isinstance(widget, QRadioButton):
                    widget.clicked.connect(partial(calculate_avg, substansive_mark_dict=substansive_mark_dict,
                                                   label=avarage_mark))
            row += 1

        self.in_frame_layout.addWidget(QLabel('Średnia ocena zajęć: '), row, 0)

        substansive_mark_dict['Średnia ocena zajęć: '] = avarage_mark

        self.in_frame_layout.addWidget(avarage_mark, row, 1)

        row += 1

        row = self.add_empty_widget(row)

        self.in_frame_layout.addWidget(QLabel('Ocena końcowa: '), row, 0)

        final_mark_template = ['wzorowa', 'bardzo dobra', 'dobra', 'dostateczna', 'negatywna']
        group1 = QHBoxLayout()
        group = QGroupBox()
        for mark in final_mark_template:
            group1.addWidget(QRadioButton(mark))
        group.setLayout(group1)
        self.in_frame_layout.addWidget(group, row, 1, 1, 2)
        row += 1

        substansive_mark_dict['Ocena końcowa: '] = group

        self.in_frame_layout.addWidget(QLabel('Wnioski i zalecenia: '), row, 0)

        solution = QTextEdit('')
        self.in_frame_layout.addWidget(solution, row, 1, 1, 2)

        substansive_mark_dict['Wnioski i zalecenia: '] = solution

        row += 1
        self.in_frame_layout.addWidget(btn_back, row, 0)
        self.in_frame_layout.addWidget(btn_accept, row, 1, 1, 2)

    def add_empty_widget(self, row):
        empty_widget = QWidget()
        empty_widget.setFixedSize(QSize(100, 25))

        self.in_frame_layout.addWidget(empty_widget, row, 0)
        row += 1
        return row

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
        self.in_frame_layout.addWidget(QLabel("Czy chcesz zaakceptować wyniki?"), 0, 0, 2, 1)
        self.in_frame_layout.addWidget(btn_accept, 1, 0)
        self.in_frame_layout.addWidget(btn_cancellation, 1, 1)
        btn_accept.clicked.connect(partial(self.accept_results, result=result))
        btn_cancellation.clicked.connect(partial(self.write_appeal_from_protocol_results, result=result))

    def accept_results(self, result):
        self.clear_in_frame_layout()
        btn_print = QPushButton("Wydrukuj protokół")
        textEditor = QTextEdit()
        btn_upload = QPushButton("Załącz plik")
        btn_accept = QPushButton("Wyślij")
        self.in_frame_layout.addWidget(btn_print, 1, 0)
        self.in_frame_layout.addWidget(btn_upload, 1, 1)
        self.in_frame_layout.addWidget(textEditor, 0, 0, 1, 3)
        btn_print.clicked.connect(partial(print_results, result=result))
        btn_upload.clicked.connect(partial(self.get_text_file, textEditor=textEditor, btn_accept=btn_accept,
                                           id_pro=result.id))

    def send_accepted_results(self, file_name, id_pro):
        f = open(file_name, "a")
        f.writelines("\nData akceptacji: "+str(date.today()))
        f.close()
        self.protocol_result_list.list[self.protocol_result_list.get_index_by_id(id_pro)].status = 0
        self.clear_in_frame_layout()
        send_accepted_protocol(file_name)

    def get_text_file(self, textEditor, btn_accept, id_pro):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Txt File', r"ProtocolsAccepted",
                                                   "Text files (*.txt)")
        if(file_name.endswith('.txt')):
            with open(file_name, 'r') as f:
                data = f.read()
                textEditor.setPlainText(data)
                f.close()
            self.in_frame_layout.addWidget(btn_accept, 1, 2)
            btn_accept.clicked.connect(partial(self.send_accepted_results, file_name=file_name, id_pro=id_pro))
        else:
            pass

    def write_appeal_from_protocol_results(self, result):
        self.clear_in_frame_layout()
        text_editor = QTextEdit()
        label = QLabel("Treść odwołania")
        btn_accept = QPushButton("Wyślij")

        self.in_frame_layout.addWidget(label, 0, 0)
        self.in_frame_layout.addWidget(text_editor, 0, 1, 1, 2)
        self.in_frame_layout.addWidget(btn_accept, 1, 2)

        btn_accept.clicked.connect(partial(self.send_appeal_from_protocol_results, result=result, text_editor=text_editor))

    def send_appeal_from_protocol_results(self, result, text_editor):
        self.clear_in_frame_layout()
        self.protocol_result_list.list[self.protocol_result_list.get_index_by_id(result.id)].status = 2
        create_appeal_from_protocol(text_editor.toPlainText(), result)

    def view_and_sort_protocols(self):
        self.clear_in_frame_layout()

        frame = QFrame()
        frame.setFixedHeight(18)
        frame.setStyleSheet('border: 1px solid black')

        sort_list = QComboBox()
        sort_list.addItems(['Brak', 'Rosnąco', 'Malejąco'])

        sort_by_list = QComboBox()
        sort_by_list.addItems(['nr Protokołu', 'Prowadzący', 'Data hospitacji', 'Ocena pracownika'])

        self.in_frame_layout.addWidget(QLabel('Sortowanie: '), 0, 0)
        self.in_frame_layout.addWidget(sort_list, 0, 1)
        self.in_frame_layout.addWidget(QLabel('według: '), 0, 2)
        self.in_frame_layout.addWidget(sort_by_list, 0, 3)

        self.in_frame_layout.addWidget(frame, 1, 0, 1, 6)
        self.in_frame_layout.addWidget(QLabel('nr Protokołu'), 1, 0)
        self.in_frame_layout.addWidget(QLabel('Prowadzący'), 1, 1)
        self.in_frame_layout.addWidget(QLabel('Data hospitacji'), 1, 2)
        self.in_frame_layout.addWidget(QLabel('Ocena pracownika'), 1, 3)

        protocols = []
        path = f'{os.getcwd()}\\Protocols'
        for r, d, f in os.walk(path):
            for file in f:
                if '.json' in file:
                    protocols.append(os.path.join(r, file))

        protocols_in_dir = {

        }
        for protocol in protocols:
            with open(protocol, 'r', encoding='utf-8') as file:
                protocol_number = os.path.basename(protocol).split('_')[1].split('.')[0]
                protocols_in_dir[protocol_number] = json.load(file)

        sort_list.currentIndexChanged.connect(partial(self.sort_by_chosen,
                                                      order=sort_list,
                                                      order_by=sort_by_list,
                                                      protocols_to_sort=protocols_in_dir))
        sort_by_list.currentIndexChanged.connect(partial(self.sort_by_chosen,
                                                         order=sort_list,
                                                         order_by=sort_by_list,
                                                         protocols_to_sort=protocols_in_dir))

        self.view_sorted_protocols(protocols_in_dir)

    def sort_by_chosen(self, order, order_by, protocols_to_sort):
        order = order.currentText()
        order_by = order_by.currentText()
        print(f'{order_by} {order}')

    def view_sorted_protocols(self, sorted_protocol_list):
        row = 2

        for number, protocol in sorted_protocol_list.items():
            self.in_frame_layout.addWidget(QLabel(number), row, 0)
            self.in_frame_layout.addWidget(QLabel(protocol['Prawadzący zajęcia/Jednostka organizacyjna']), row, 1)
            self.in_frame_layout.addWidget(QLabel(protocol['Data otrzymania']), row, 2)
            self.in_frame_layout.addWidget(QLabel(protocol['Ocena merytoryczna']['Ocena końcowa'] + ' (' +
                                                  protocol['Ocena merytoryczna']['Średnia ocena zajęć'] + ')'), row, 3)
            row += 1
