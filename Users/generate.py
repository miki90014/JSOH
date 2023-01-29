from random import randint
import json

imie_list = ['Piotr', 'Jan', 'Małgorzata', 'Krzysztof', 'Hanna', 'Michał', 'Ryszard', 'Alicja', 'Marzena', 'Kacper']
nazwisko_list = ['Kuśnierz', 'Nowak', 'Wojcieszak', 'Wąs', 'Pieńkowski', 'Wiktorowski', 'Kowalski', 'Wójcik',
                 'Kowalczyk', 'Woźniak']

for i in range(1, 21):
    person = {
        'Id': i,
        'Imie': imie_list[randint(0, 9)],
        'Nazwisko': nazwisko_list[randint(0, 9)]
    }
    with open(f'{i}.json', 'w', encoding='utf-8') as f:
        json.dump(person, f, indent=4, ensure_ascii=False)
