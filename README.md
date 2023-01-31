# JSOH

Wszelkie pliki będą przechowywane w formacie. 
W podanych folderach znajdują się pliki odczytywane przez aplikacje:
- `Classes\ `
- `Employees\ `
- `Inspections\ `
- `Protocols\ `
- `Protocols99\ `
- `ProtocolsAccepted\ `
- `ProtocolsAppeal\ `
- `Schedules\ `
- `TestData\ `
- `TestFiles\ `

## Classes

W `Classes\ ` są przechowywane pliki z informacjami dotyczących zajęć.
Nazwa pliku jest numerem `id` zajęć.

## Employees

W `Employees\ ` są przechowywane pliki z informacjami dotyczącymi pracowników.
Nazwa pliku jest numerem `id` pracownika.

## Inspection

W `Inspection\ ` są przechowywane pliki z informacjami dotyczącymi hospitacji.
Nazwa pliku jest numerem `id` hospitacji.

## Protocols

W `Protocols\ ` są przechowywane pliki z informacjami dotyczącymi protokołów.
Nazwy plików są przyjęta z konwencją `protocol_x.json` gdzie `x` jest numerem `id` protokołu.

## Protocols99

W `Protocols99\ ` są przechowywane pliki z informacjami dotyczącymi protokołów hospitowanego o numerze `id: 99`.
Dla uproszczenia aplikacji, zostały one wygenerowane wcześniej. 
Nazwy plików są przyjęta z konwencją `protocol_x.json` gdzie `x` jest numerem `id` protokołu.

## ProtocolsAccepted

W `ProtocolsAccepted\ ` są przechowywane pliki z informacjami dotyczącymi wszystkich protokołów zaakceptowanych.
Jest to kopia protokołu rozszerzona o podpis. Jest to imitacja "podpisanych protokołów" (np. zeskanowanych dokumentów z odręcznym podpisem pracownika).
Nazwy plików są przyjęta z konwencją `accepted_protocol_x.json` gdzie `x` jest numerem `id` protokołu.

## ProtocolsAppeal

W `ProtocolsAppeal\ ` są przechowywane pliki z informacjami dotyczącymi wszystkich odwołań. 
Nazwy plików są przyjęta z konwencją `appeal_from_protocol_x.json` gdzie `x` jest numerem `id` protokołu.

## Schedules

W `Schedules\ ` są przechowywane pliki z informacjami dotyczącymi harmonogramu hospitacji.

## TestData

W `TestData\ ` są przechowywane pliki, które są wykorzystywane w testach jednostkowych zanjdujących się w pliku `test_ewa.py`

## TestFiles

W `TestData\ ` są przechowywane pliki, które są wykorzystywane w testach jednostkowych zanjdujących się w pliku `test_monika.py`