
from datetime import date
from random import randrange


class ProtocolResult:
    id = randrange(1, 100)
    received_date = date.today()
    accepted_date = date.today()
    status = randrange(0, 4)
