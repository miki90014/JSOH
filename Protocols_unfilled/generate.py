from random import randint
import json
import os

people = []
path = f'{os.getcwd()}\\..\\Users'
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            people.append(os.path.join(r, file))

people_in_dir = []

for protocol in people:
    with open(protocol, 'r', encoding='utf-8') as file:
        people_in_dir.append(json.load(file))

print(people_in_dir)

lista_kierunkow = ['Projektowanie oprogramowania', 'Podstawy internetu rzeczy', 'Techniki prezentacji',
                   'Algorytmy i struktury danych', 'Architektura komputerów', 'Projektowanie aplikacji mobilnych',
                   'Projektowanie gier', 'Algebra', 'Analiza']

semestry = ['Lato 2022/2023', 'Zima 2022/2023', 'Lato 2021/2022', 'Zima 2021/2022', 'Lato 2020/2021', 'Zima 2020/2021']

for i in range(1, 31):
    liczba = randint(0, 19)
    protocol = {
        'Nr protokołu': f'{0 if i < 10 else ""}{i}',
        'Nr hospitacji': 'unknown',
        'Prowadzący zajęcia/Jednostka organizacyjna': people_in_dir[liczba]['Nazwisko'] + ' ' + people_in_dir[liczba]
                                                                                                             ['Imie'],
        "Nazwa kursu/kierunek studiów": lista_kierunkow[randint(0, 8)],
        "Kod kursu": "IST-023",
        "Forma dydaktyczna": f'{"wykład" if randint(0, 1) == 0 else "inna"}',
        "Sposób realizacji": f'{"tradycyjny" if randint(0, 1) == 0 else "zdalna"}',
        "Stopień i forma studiów": f'{"I" if randint(0, 1) == 0 else "II"} stopień',
        "Semestr": semestry[randint(0, 5)],
        "Miejsce i termin zajęć": "Budynek B2, sala 152, wt 13:15-14:45",
        "Środowisko realizacji zajęć": "Nie dotyczy"
    }

    with open(f'protocol_{0 if i < 10 else ""}{i}.json', 'w', encoding='utf-8') as f:
        json.dump(protocol, f, indent=4, ensure_ascii=False)
