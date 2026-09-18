import json
import datetime 

class VypozicanaKniha:
    def __init__(self, kniha, datum_vypozicania, datum_vratenia):
        self.kniha = kniha
        self.datum_vypozicania = datum_vypozicania
        self.datum_vratenia = datum_vratenia
        self.kniha.je_vypozicana = True
    def vratit(self):
        self.kniha.je_vypozicana = False
        print(f'Kniha {self.kniha.nazov} bola vrátená do knižnice.')
        log = {'kniha': self.kniha.nazov, 'datum_vypozicania': self.datum_vypozicania, 'datum_vratenia': self.datum_vratenia, 'vratena': datetime.now().strftime("%Y-%m-%d %H:%M:%S") }
        with open('data.json', 'w') as f:
          json.dump(log, f)
        del self