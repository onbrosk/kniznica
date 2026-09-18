from datetime import date, timedelta


class Clen:

    posledne_id = 0

    def __init__(self, meno: str, priezvisko: str, datum_narodenia: date, dlzka_clenstva: int = 365):
        self.id_clena = None

        self.meno = meno
        self.priezvisko = priezvisko
        self.datum_narodenia = datum_narodenia
        self.dlzka_clenstva = dlzka_clenstva  # dni

        self.datum_vzniku = None
        self.koniec_clenstva = None
        self.aktivny = False

        self.vypozicane_knihy = []

    def vytvorit_konto(self):
        if self.aktivny:
            print("Konto už existuje a je aktívne.")
            return

        Clen.posledne_id += 1
        self.id_clena = Clen.posledne_id

        self.datum_vzniku = date.today()
        self.koniec_clenstva = date.today() + timedelta(days=self.dlzka_clenstva)
        self.aktivny = True

        print(f"Konto pre {self.meno} {self.priezvisko} bolo vytvorené (#{self.id_clena}).")

    def predlzit_konto(self, dni: int = 365):
        if not self.aktivny:
            print("Konto nie je aktívne, najprv ho treba vytvoriť.")
            return
        self.koniec_clenstva += timedelta(days=dni)
        print(f"Konto predĺžené o {dni} dní, platí do {self.koniec_clenstva}.")

    def zrusit_konto(self):
        if not self.aktivny:
            print("Konto už nie je aktívne.")
            return
        if self.vypozicane_knihy:
            print("Konto nemožno zrušiť, člen má vypožičané knihy.")
            return
        self.aktivny = False
        print(f"Konto pre {self.meno} {self.priezvisko} bolo zrušené.")

    def __str__(self):
        stav = "aktívne" if self.aktivny else "neaktívne/zrušené"
        return (f"Člen #{self.id_clena}: {self.meno} {self.priezvisko}, "
                f"konto {stav}" + (f" do {self.koniec_clenstva}" if self.aktivny else ""))