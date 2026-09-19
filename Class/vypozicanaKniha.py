import json
import datetime 

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class VypozicanaKniha:
    def __init__(self, kniha: isinstance, clen: isinstance, datum_vypozicania, datum_vratenia ):
        self.kniha = kniha
        self.clen = clen
        self.datum_vypozicania = datum_vypozicania
        self.datum_vratenia = datum_vratenia
        self.kniha.je_vypozicana = True
    def __str__(self):
        return f"{self.kniha.nazov} od {self.kniha.autor}, vypožičaná dňa {self.datum_vypozicania} a vrátená dňa {self.datum_vratenia}"
    def vratit(self):
        self.kniha.je_vypozicana = False
        print(f'Kniha {self.kniha.nazov} bola vrátená do knižnice.')
        log = {'kniha': self.kniha.nazov, 'kniha_id': self.kniha.id, 'clen': f'{self.clen.meno} {self.clen.priezvisko}', 'datum_vypozicania': self.datum_vypozicania, 'datum_vratenia': self.datum_vratenia, 'vratena': timestamp}
        with open('data.json', 'w',  encoding='utf-8') as f:
          json.dump(log, f)
          f.close()
        del self