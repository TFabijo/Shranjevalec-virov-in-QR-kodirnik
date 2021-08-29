from datetime import date

class Model:
    def __init__(self):
        self.teme = []
    def dodaj_temo(self, tema):
        self.teme.append(tema)
    def izbriši_temo(self,tema):
        self.teme.remove(tema)
class Tema:
    def __init__(self,ime):
        self.ime = ime
        self.viri = []
    def dodaj_vir(self,vir):
        self.viri.append(vir)
    def odstrani_vir(self,vir):
        self.viri.remove(vir)

class Viri:
    def __init__(self,ime,opis,datum = date.today()):
        self.ime = ime
        self.opis = opis
        self.datum = f"{datum.day}.{datum.month}.{datum.year}"

class QR_kodirnik:
    def __init__(self,vir,ime_slike):
        self.vir = vir
        self.ime_slike = ime_slike
        