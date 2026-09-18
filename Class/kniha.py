class Kniha:
    def __init__(self, nazov, autor, rok_vydania, zaner, jazyk, poskodenie, je_vypozicana, isbn):
        self.nazov = nazov
        self.autor = autor
        self.rok_vydania = rok_vydania
        self.zanre = zaner
        self.jazyk = jazyk
        self.poskodenie = poskodenie
        self.je_vypozicana = je_vypozicana
        self.isbn = isbn

    def odobrat(self):
        del self
        print(f'Kniha {self.nazov} bola odobratá z knižnice.')

    def aktualizovat(self):
        self.nazov = input("Zadajte nový názov knihy: ")
        self.autor = input("Zadajte nového autora knihy: ")
        self.rok_vydania = input("Zadajte nový rok vydania knihy: ")
        self.zanre = input("Zadajte nový žáner knihy: ")
        self.jazyk = input("Zadajte nový jazyk knihy: ")
        self.poskodenie = input("Zadajte nové poškodenie knihy (True/False): ")
        self.je_vypozicana = input("Zadajte, či je kniha vypožičaná (True/False): ")
        self.isbn = input("Zadajte nové ISBN knihy: ")

    def aktualizovat_poskodenie(self, poskodenie):
        self.poskodenie = poskodenie

    def nahradit(self, cena_nahradenia):
        self.cena_nahradenia = cena_nahradenia
        
    def ziskaj_data(self):
        return [self.nazov, self.autor, self.rok_vydania, self.zaner, self.jazyk, self.poskodenie, self.je_vypozicana, self.isbn]
  
    def __str__(self):
        return f"{self.nazov} od {self.autor}, vydaná v roku {self.rok_vydania}"
