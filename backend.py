from Class.Kniha import Kniha
from Class.vypozicanaKniha import VypozicanaKniha

kniha1 = Kniha("Cudzinec", "Albert Camus", "2008", "Filozofický román", 'slovenský', 'stredné', False, "978-0451524935")
kniha2 = Kniha("Cudzinesdsdc", "Albert Camusss", "2008", "Filozofický román", 'slovenský', 'stredné', False, "978-0451524935")
knihy = [
  kniha1,
  kniha2
]

vypozicane = []
VypozicanaKniha1 = VypozicanaKniha(kniha1, "2023-01-01", "2023-01-15")