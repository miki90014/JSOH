import os
import json
from datetime import date, datetime
from functools import partial

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import *
from Model.example_data import *


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
    values = []
    for buttons in substansive_mark_dict.values():
        for child in buttons.children():
            if isinstance(child, QRadioButton):
                try:
                    values.append(float(child.text() if child.isChecked() else 0))
                except ValueError:
                    pass
    value = avg(values)
    label.setText(str(value))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('JSOH')
        # for now
        self.protocol_result_list = ProtocolResultList(99)

        self.protocol_list = ProtocolList(20)

        self.main_layout = QGridLayout()

        self.right_side_menu = QVBoxLayout()

        self.right_side_menu_button_list = [QPushButton('Przegląd zaplanowanych hospitacji'), QPushButton('Hospitacje'),
                                            QPushButton('Wgląd do wyników hospitacji'),
                                            QPushButton('Ocena pracowników')]

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
        for _ in range(len(self.protocol_result_list.list)):
            button_list.append(QPushButton('Wgląd'))

        for result in self.protocol_result_list.list:
            self.in_frame_layout.addWidget(QLabel(str(result.id)), row, 0)
            self.in_frame_layout.addWidget(QLabel(str(result.received_date)), row, 1)
            self.in_frame_layout.addWidget(QLabel(str(result.accepted_date)), row, 2)
            self.in_frame_layout.addWidget(QLabel(str(result.status)), row, 3)

            button_list[row - 1].clicked.connect(partial(self.view_specific_protocolc, result=result))
            self.in_frame_layout.addWidget(button_list[row - 1], row, 4)
            row += 1

    def view_specific_protocolc(self, result):
        self.clear_in_frame_layout()
        btn_back = QPushButton("Wróć do listy")
        btn_back.clicked.connect(self.view_protocol_results)

        row = 0
        f = open(result.path_to_file, encoding="utf-8")
        data = json.load(f)
        for label in data:
            self.in_frame_layout.addWidget(QLabel(str(label)), row, 0)
            if str(label) == "Ocena formalna":
                row += 1
                for l in data["Ocena formalna"]:
                    self.in_frame_layout.addWidget(QLabel(str(l)), row, 1)
                    self.in_frame_layout.addWidget(QLabel(str(data["Ocena formalna"][str(l)])), row, 2)
                    row += 1
            elif str(label) == "Ocena merytoryczna":
                row += 1
                for l in data["Ocena formalna"]:
                    self.in_frame_layout.addWidget(QLabel(str(l)), row, 1)
                    self.in_frame_layout.addWidget(QLabel(str(data["Ocena formalna"][str(l)])), row, 2)
                    row += 1
            else:
                self.in_frame_layout.addWidget(QLabel(str(data[str(label)])), row, 1)
            row += 1
        f.close()
        self.in_frame_layout.addWidget(btn_back, 0, 3)

        if result.status == STATUS_TO_ACCEPT:
            answer_results = QPushButton('Odpowiedz na wyniki')
            answer_results.clicked.connect(lambda: self.answer_results(result))
            self.in_frame_layout.addWidget(answer_results, 0, 3)
        else:
            alert = QMessageBox()
            alert.setText('Wyświetlany protokół zotsał zaakceptowany lub jest w trakcie odwołania.\n'
                          'Nie możesz podjąć żadnych akcji.')
            alert.exec()

    def view_protocols_to_fill(self):
        self.clear_in_frame_layout()

        protocols = load_unfilled_protocols()

        button_list = []

        frame = QFrame()
        frame.setStyleSheet('border: 1px solid black')

        self.in_frame_layout.addWidget(frame, 0, 0, 1, 6)
        self.in_frame_layout.addWidget(QLabel('nr Protokołu'), 0, 0)
        self.in_frame_layout.addWidget(QLabel('Prowadzący'), 0, 1)
        self.in_frame_layout.addWidget(QLabel('Data hospitacji'), 0, 2)

        row = 1
        for _ in range(len(protocols)):
            button_list.append(QPushButton('Wypełnij'))

        for _, protocol in protocols.items():
            self.in_frame_layout.addWidget(QLabel(protocol['Nr protokołu']), row, 0)
            self.in_frame_layout.addWidget(QLabel(protocol['Prowadzący zajęcia/Jednostka organizacyjna']), row, 1)
            self.in_frame_layout.addWidget(QLabel(datetime.today().strftime('%Y-%m-%d')), row, 2)
            self.in_frame_layout.addWidget(QLabel('Do Wypełnienia'), row, 3)
            self.in_frame_layout.addWidget(QLabel(protocol['Forma dydaktyczna']), row, 4)
            button_list[row - 1].clicked.connect(partial(self.fill_protocol, result=protocol))
            self.in_frame_layout.addWidget(button_list[row - 1], row, 5)
            row += 1

    def stop_filling_protocol(self):
        alert = QMessageBox()
        alert.setText('Anulowano wypełnianie protokołu')
        alert.exec()
        self.view_protocols_to_fill()

    def save_protocol(self, result, basic_info, formal_mark, substansive_mark):
        save_protocol_to_file(result, basic_info, formal_mark, substansive_mark)

        alert = QMessageBox()
        alert.setText('Zapisano protokół')
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
        self.in_frame_layout.addWidget(QLabel(result['Nr protokołu']), 0, 1)

        basic_info = [QLabel(f'Prowadzący zajęcia/Jednostka organizacyjna '
                             f'{result["Prowadzący zajęcia/Jednostka organizacyjna"]}'),
                      QLabel(f'Nazwa kursu/kierunek studiów {result["Nazwa kursu/kierunek studiów"]}'),
                      QLabel(f'Kod kursu {result["Kod kursu"]}'),
                      QLabel(f'Forma dydaktyczna {result["Forma dydaktyczna"]}'),
                      QLabel(f'Sposób realizacji {result["Sposób realizacji"]}'),
                      QLabel(f'Stopień i forma studiów {result["Stopień i forma studiów"]}'),
                      QLabel(f'Semestr {result["Semestr"]}'),
                      QLabel(f'Miejsce i termin zajęć {result["Miejsce i termin zajęć"]}'),
                      QLabel(f'Srodowisko realizacji zajęć {result["Środowisko realizacji zajęć"]}')]

        basic_info_for_save = {
            'Prowadzący zajęcia/Jednostka organizacyjna': result["Prowadzący zajęcia/Jednostka organizacyjna"],
            'Id Prowadzącego': result["Id Prowadzącego"],
            'Nazwa kursu/kierunek studiów': result["Nazwa kursu/kierunek studiów"],
            'Kod kursu': result["Kod kursu"],
            'Forma dydaktyczna': result["Forma dydaktyczna"],
            'Sposób realizacji': result["Sposób realizacji"],
            'Stopień i forma studiów': result["Stopień i forma studiów"],
            'Semestr': result["Semestr"],
            'Miejsce i termin zajęć': result["Miejsce i termin zajęć"],
            'Srodowisko realizacji zajęć': result["Środowisko realizacji zajęć"]
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
                        widget.clicked.connect(lambda: show_fields(buttons_delay, delay_label, delay, True))
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

        if result["Forma dydaktyczna"] == "wykład":
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
        group1.itemAt(4).widget().setChecked(True)
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
        text_editor = QTextEdit()
        btn_upload = QPushButton("Załącz plik")
        btn_accept = QPushButton("Wyślij")
        self.in_frame_layout.addWidget(btn_print, 1, 0)
        self.in_frame_layout.addWidget(btn_upload, 1, 1)
        self.in_frame_layout.addWidget(text_editor, 0, 0, 1, 3)
        btn_print.clicked.connect(partial(print_results, result=result))
        btn_upload.clicked.connect(partial(self.get_text_file, text_editor=text_editor, btn_accept=btn_accept,
                                           path=result.path_to_file))

    def send_accepted_results(self, file_name, path):
        f = open(path, encoding="utf-8")
        data = json.load(f)
        f.close()
        f = open(path, "w", encoding="utf-8")
        data["Status protokołu"] = STATUS_ACCEPTED
        data["Nr akceptacji"] = data["Nr protokołu"]
        data["Data akceptacji"] = str(date.today())
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()
        self.protocol_result_list.list[self.protocol_result_list.get_index_by_id(data["Nr protokołu"])].reload_data()

        self.clear_in_frame_layout()
        send_accepted_protocol(file_name)

    def get_text_file(self, text_editor, btn_accept, path):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Txt File', r"ProtocolsAccepted",
                                                   "Text files (*.txt)")
        if file_name.endswith('.txt'):
            with open(file_name, 'r', encoding="utf-8") as f:
                data = f.read()
                text_editor.setPlainText(data)
                f.close()
            self.in_frame_layout.addWidget(btn_accept, 1, 2)
            btn_accept.clicked.connect(partial(self.send_accepted_results, file_name=file_name, path=path))
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

        btn_accept.clicked.connect(
            partial(self.send_appeal_from_protocol_results, result=result, text_editor=text_editor))

    def send_appeal_from_protocol_results(self, result, text_editor):
        self.clear_in_frame_layout()
        create_appeal_from_protocol(text_editor.toPlainText(), result)
        self.protocol_result_list.list[self.protocol_result_list.get_index_by_id(result.id)].reload_data()

    def view_and_sort_protocols(self):
        self.clear_in_frame_layout()

        frame = QFrame()
        frame.setFixedHeight(18)
        frame.setStyleSheet('border: 1px solid black')

        sort_list = QComboBox()
        sort_list.addItems(['Brak', 'Rosnąco', 'Malejąco'])

        sort_by_list = QComboBox()
        sort_by_list.addItems(['nr Protokołu', 'Prowadzący', 'Data hospitacji', 'Ocena pracownika'])

        filter_list_semester = QComboBox()

        self.in_frame_layout.addWidget(QLabel('Sortowanie: '), 0, 0)
        self.in_frame_layout.addWidget(sort_list, 0, 1)
        self.in_frame_layout.addWidget(QLabel('według: '), 0, 2)
        self.in_frame_layout.addWidget(sort_by_list, 0, 3)
        self.in_frame_layout.addWidget(QLabel('dotyczące semestru: '), 0, 4)
        self.in_frame_layout.addWidget(filter_list_semester, 0, 5)

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

        all_semesters = ['Brak']
        for _, protocol in protocols_in_dir.items():
            temp = protocol['Semestr']
            if temp not in all_semesters:
                all_semesters.append(temp)

        filter_list_semester.addItems(all_semesters)

        sort_list.currentIndexChanged.connect(partial(self.sort_by_chosen,
                                                      order=sort_list,
                                                      order_by=sort_by_list,
                                                      protocols_to_sort=protocols_in_dir,
                                                      number=filter_list_semester))
        sort_by_list.currentIndexChanged.connect(partial(self.sort_by_chosen,
                                                         order=sort_list,
                                                         order_by=sort_by_list,
                                                         protocols_to_sort=protocols_in_dir,
                                                         number=filter_list_semester))
        filter_list_semester.currentIndexChanged.connect(partial(self.sort_by_chosen,
                                                                 order=sort_list,
                                                                 order_by=sort_by_list,
                                                                 protocols_to_sort=protocols_in_dir,
                                                                 number=filter_list_semester))

        self.view_sorted_protocols(protocols_in_dir)

    def sort_by_chosen(self, order, order_by, protocols_to_sort, number):
        order = order.currentText()
        order_by = order_by.currentText()
        number = number.currentText()

        sorted_protocols = sort_protocols_list(order, order_by, protocols_to_sort, number)

        self.view_sorted_protocols(sorted_protocols)

    def view_sorted_protocols(self, sorted_protocol_list):
        for i in range(self.in_frame_layout.count() - 1, -1, -1):
            if i >= 11:
                self.in_frame_layout.itemAt(i).widget().setParent(None)
        row = 2

        if len(sorted_protocol_list) == 0:
            self.in_frame_layout.addWidget(QLabel("Wystąpił błąd, brak aktualnie dostępnych protokołów hospitacji"))
            return False

        for number, protocol in sorted_protocol_list.items():
            self.in_frame_layout.addWidget(QLabel(number), row, 0)
            self.in_frame_layout.addWidget(QLabel(protocol['Prowadzący zajęcia/Jednostka organizacyjna']), row, 1)
            self.in_frame_layout.addWidget(QLabel(protocol['Data otrzymania']), row, 2)
            self.in_frame_layout.addWidget(QLabel(protocol['Ocena merytoryczna']['Ocena końcowa']), row, 3)
            row += 1

        return True
