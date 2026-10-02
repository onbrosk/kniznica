import json
import datetime 

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class VypozicanaKniha:
    def __init__(self, kniha: isinstance, clen: isinstance, datum_vypozicania, datum_vratenia, datum_realneho_vratenia=None, zapis_do_logu=True):
        self.kniha = kniha
        self.clen = clen
        self.datum_vypozicania = datum_vypozicania
        self.datum_vratenia = datum_vratenia
        self.datum_realneho_vratenia = datum_realneho_vratenia
        self.kniha.je_vypozicana = datum_realneho_vratenia is None
        if zapis_do_logu:
            self._zapisat_vypozicanie()

    def _zapisat_vypozicanie(self):
        cesta = 'data/logs/vypozicane.json'
        try:
            with open(cesta, 'r', encoding='utf-8') as f:
                zaznamy = json.load(f)
        except FileNotFoundError:
            zaznamy = []

        if not isinstance(zaznamy, list):
            zaznamy = [zaznamy]

        zaznamy.append({
            'kniha': self.kniha.nazov,
            'kniha_id': self.kniha.id,
            'clen': f'{self.clen.meno} {self.clen.priezvisko}',
            'clen_id': self.clen.id,
            'datum_vypozicania': str(self.datum_vypozicania),
            'datum_vratenia': str(self.datum_vratenia),
            'datum_realneho_vratenia': '',
            'vytvorene': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        with open(cesta, 'w', encoding='utf-8') as f:
            json.dump(zaznamy, f, ensure_ascii=False, indent=2)

    def __str__(self):
        return f"{self.kniha.nazov} od {self.kniha.autor}, vypožičaná dňa {self.datum_vypozicania} a vrátená dňa {self.datum_vratenia}"

    def vratit(self):
        self.datum_realneho_vratenia = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.kniha.je_vypozicana = False

        cesta = 'data/logs/vypozicane.json'
        with open(cesta, 'r', encoding='utf-8') as f:
            zaznamy = json.load(f)

        if not isinstance(zaznamy, list):
            zaznamy = [zaznamy]

        for zaznam in reversed(zaznamy):
            if (
                str(zaznam.get('kniha_id')) == str(self.kniha.id)
                and str(zaznam.get('clen_id')) == str(self.clen.id)
                and zaznam.get('datum_vypozicania') == str(self.datum_vypozicania)
            ):
                zaznam['datum_realneho_vratenia'] = self.datum_realneho_vratenia
                break

        with open(cesta, 'w', encoding='utf-8') as f:
            json.dump(zaznamy, f, ensure_ascii=False, indent=2)