import json
from Class.Kniha import Kniha
from Class.VypozicanaKniha import VypozicanaKniha
from Class.Clen import Clen


knihy = []
clenovia = []
vypozicane = []
##VypozicanaKniha1 = VypozicanaKniha(kniha1, clen1,"2023-01-01", "2023-01-15")

def zjednodus(text):
    return text.lower().replace(" ", "")

def najdi_knihu(text):
    najdene = []
    zjednoduseny_text = zjednodus(text)
    for kniha in knihy:
        if zjednoduseny_text in zjednodus(kniha.nazov):
            najdene.append(kniha);
        if zjednoduseny_text in zjednodus(kniha.autor):
            najdene.append(kniha);  
    return najdene

def najdi_podla_id(id_hodnota, array):
    if id_hodnota is None:
        return None

    for v in array:
        try:
            if str(v.id) == str(id_hodnota):
                return v
        except AttributeError:
            continue
    return None

def nacitaj_z_uloziska():
    global knihy
    global clenovia
    global vypozicane

    with open('data/knihy.json', 'r', encoding='utf-8') as f:
        ulozene_knihy = json.load(f)

    if ulozene_knihy:
        knihy = [
            Kniha(kniha['id'], kniha['nazov'], kniha['autor'], kniha['rok_vydania'], kniha['zaner'],
                        kniha['jazyk'], kniha['poskodenie'], kniha['je_vypozicana'], kniha['isbn'])
            for kniha in ulozene_knihy
        ]

    with open('data/clenovia.json', 'r', encoding='utf8') as f:
        ulozeny_clenovia = json.load(f)

    if ulozeny_clenovia:
        clenovia = [
            Clen(clen['id'], clen['meno'], clen['priezvisko'], clen['datum_narodenia'], clen['koniec_clenstva'])
            for clen in ulozeny_clenovia
        ]

    with open('data/vypozicane.json', 'r', encoding='utf-8') as f:
        ulozene_vypozicane = json.load(f)

    if ulozene_vypozicane:
        vypozicane = []
        for vypozicana in ulozene_vypozicane:
            kniha_obj = najdi_podla_id(vypozicana.get('kniha_id'), knihy)
            clen_obj = najdi_podla_id(vypozicana.get('clen_id'), clenovia)
            if kniha_obj is None or clen_obj is None:
                print(f"Vynechaný záznam: kniha_id={vypozicana.get('kniha_id')}, clen_id={vypozicana.get('clen_id')}")
                continue

            vypozicane.append(
                VypozicanaKniha(kniha_obj, clen_obj, vypozicana['datum_vypozicania'], vypozicana['datum_vratenia'])
            )
 
nacitaj_z_uloziska()
