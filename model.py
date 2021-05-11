import json

STEVILO_DOVOLJENIH_NAPAK = 9
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZACETEK = 'z'
ZMAGA, PORAZ = 'w', 'x'

class Igra:
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke is None:
            self.crke = []
        else:
            self.crke = crke

    def napacne_crke(self):
        return [c for c in self.crke if c.upper() not in self.geslo.upper()]

    def pravilne_crke(self):
        return [c for c in self.crke if c.upper() in self.geslo.upper()]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def zmaga(self):
        return not self.poraz() and len(set(self.pravilne_crke())) == len(set(self.geslo))

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def pravilni_del_gesla(self):
        pravilno = ''
        for c in self.geslo:
            if c.upper() in self.crke:
                pravilno += c
            else:
                pravilno += '_ '
        return pravilno

    def nepravilni_ugib(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        elif crka in self.geslo.upper():
            self.crke.append(crka)
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        else:
            self.crke.append(crka)
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA

with open('besede.txt', encoding='utf-8') as f:
    bazen_besed = f.read().split()

import random

def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)

class Vislice:
    datoteka_s_stanjem = 'stanje.json'

    def __init__(self):
        self.igre = {}

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        id_igre = self.prost_id_igre()
        igra = nova_igra()   
        self.igre[id_igre] = (igra, ZACETEK)
        return id_igre

    def ugibaj(self, id_igre, crka):
        igra, _ = self.igre[id_igre]
        stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, stanje)

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, encoding='utf-8') as f:
            igre = json.load(f)
        for id_igre in igre:
            geslo = igre[id_igre]['geslo']
            crke = igre[id_igre]['crke']
            stanje = igre[id_igre]['stanje']

            igra = Igra(geslo)
            igra.crke = crke

            self.igre[int(id_igre)] = (igra, stanje)

    def zapisi_igre_v_datoteko(self):
        igre = {}
        for id_igre in self.igre:
            igra, stanje = self.igre[id_igre]
            igra_slovar = {'geslo': igra.geslo, 'crke': igra.crke, 'stanje': stanje}
            igre[id_igre] = igra_slovar
        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            json.dump(igre, f)
            