# JSOH

Naszą "bazą danych" będzie folder `Database\`.
`Database\` będzie się składało (jak na razie, aby podać przykład działania):
 - `protocols.csv` 
 - `workers.csv`
 - `accepted_protocols.csv`
 - `appeal_from_protocols.csv`
 - `auditing.csv`

Pliki te one przechowywać informacje które będziemy używać w aplikacji

## protocols.csv

Praktycznie przepisany diagram klasy `Protokół z hospitacji` poszerzony o kilka kluczy obcych.
A dokładniej będzie się składać z następujących pól:

**_NOTE:_**
pamiętajcie o podanej kolejności - jeśli chcecie zmienić, wprowadźcie zmiany do `README.md` (lub jak chcecie dodać coś nowego)

- **nr protokołu** - `klucz`
- **nr hospitacji** - `klucz obcy`
- **ocena końcowa**
- **ocena merytoryczna**
- **ocena formalna**
- **wnioski i zalecenia**
- **inne uwagi**
- **forma zajęć** 
- **środowisko** 
- **kod kursu**
- **nazwa**
- **status protokołu**
- **data otrzymania**
- **nr akceptacji** - `klucz obcy` (puste jak nie ma akceptacji)
- **nr odwołania** - `klucz obcy` (puste jak nie ma odwołania)

## workers.csv

Wszystkie pola co mamy w diagramie klas `Pracownik` + `klucz glowny` **nr pracownika** jako pierwsze pole, reszta kolejność z diagramu

## accepted_protocols.csv

Wszystkie pola co mamy w diagramie klas `Akceptacja protokołu hospitacji` + `klucz glowny` **nr akceptacji** jako pierwsze pole, reszta kolejność z diagramu

## appeal_from_protocols.csv

Wszystkie pola co mamy w diagramie klas `Akceptacja protokołu hospitacji` + `klucz glowny` **nr odowołania** jako pierwsze pole, reszta kolejność z diagramu

## auditing.csv

- **nr hospitacji** - `klucz główny`
- **data hospitacji**
- **status**
- **nr pracownika** - `klucz obcy`, pracownik jako hospitujący
- **nr zespołu hospitującego** - `klucz obcy`
- **nr zajec** - `klucz obcy`

**_NOTE:_**
Zakładam że w `zajęciach` będzie się znajdować klucz obcy `Pracownika` dla hospitowanego.

Mam nadzieję że te przykłady rozjaśniły jak będziemy pracować - dodajemy klucze obce i klucze główne do naszych diagramów.
W kodzie natomaist trzeba będzie pomyśleć o klasach i nie wiem, czy będziemy je łączyć za pomocą "numerów" czy za pomocą refernecji, to jest do ustalenia.
Same diagramy poprawię później tak aby wszystko się zgadzało z implementacją. Jak macie pytania to piszcie.  

Trzeba będzie też pomyśleć o wszystkich typach enum, czy też będziemy je przechowywać jako pliki czy może przeobimy je na constraint jak np. w Oracle z płcią Kocura:
```
CREATE TABLE Kocury (
    imie VARCHAR2(15) CONSTRAINT kc_im_nn NOT NULL,
    plec VARCHAR2(1) CONSTRAINT kc_pl_ch CHECK (plec IN ('D', 'M')),
```
...