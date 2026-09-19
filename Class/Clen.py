from datetime import date, timedelta


class Clen:
    def __init__(self, id: int, meno: str, priezvisko: str, datum_narodenia: date, koniec_clenstva: date):
        self.id = id
        self.id_clena = id
        self.aktivny = True

        self.meno = meno
        self.priezvisko = priezvisko
        self.datum_narodenia = datum_narodenia

        self.koniec_clenstva = koniec_clenstva
        self.datum_vzniku = date.today()

        self.vypozicane_knihy = []

    def zmenit_dlzku_clenstva(self, datum):
        self.koniec_clenstva = datum
        
    def zrusit_konto(self):
        if self.vypozicane_knihy:
            raise Exception("Nie je možné zrušiť konto, pretože člen má stále vypožičané knihy.")
        del self

    def ziskaj_data(self):
        return [self.id, self.meno, self.priezvisko, self.datum_narodenia, self.koniec_clenstva]
    
    def __str__(self):
        stav = "aktívne" if self.aktivny else "neaktívne/zrušené"
        return (f"Člen #{self.id_clena}: {self.meno} {self.priezvisko}, "
                f"konto {stav}" + (f" do {self.koniec_clenstva}" if self.aktivny else ""))