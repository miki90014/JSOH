from datetime import date
import numpy as np


class ProtocolResult:
    def __init__(self):
        self.id = np.random.randint(100)+1
        self.received_date = date.today()
        self.accepted_date = date.today()
        self.status = np.random.randint(0, 4)
