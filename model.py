from datetime import date
import datetime
import json

class Model:
    def __init__(self):
        self.teme = []
    def dodaj_temo(self, tema):
        self.teme.append(tema)
    def izbriši_temo(self,tema):
        self.teme.remove(tema)

    def v_slovar(self):
        return {
            "teme": [tema.v_slovar() for tema in self.teme],
        }

    @staticmethod
    def iz_slovarja(slovar):
        model  = Model()
        model.teme = [
            Tema.iz_slovarja(sl_tem) for sl_tem in slovar["teme"]
        ]
        return model

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Model.iz_slovarja(slovar)

class Tema:
    def __init__(self,ime):
        self.ime = ime
        self.viri = []
    def dodaj_vir(self,vir):
        self.viri.append(vir)
    def odstrani_vir(self,vir):
        self.viri.remove(vir)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "viri": [vir.v_slovar() for vir in self.viri],
        }
    @staticmethod
    def iz_slovarja(slovar):
        tema = Tema(slovar["ime"])
        tema.viri = [
            Viri.iz_slovarja(sl_virov) for sl_virov in slovar["viri"]
        ]
        return tema

class Viri:
    def __init__(self,ime,opis,datum = date.today()):
        self.ime = ime
        self.opis = opis
        self.datum = f"{datum.day}.{datum.month}.{datum.year}"
    def v_slovar(self):
        return {
            "ime": self.ime,
            "opis": self.opis,
            "datum": self.datum ,
        }

    @staticmethod
    def iz_slovarja(slovar):
        dat = slovar["datum"].split(".")
        return Viri(
            slovar["ime"],
            slovar["opis"],
            datetime.date(int(dat[2]),int(dat[1]),int(dat[0])),
        )

class QR_kodirnik:
    def __init__(self,vir,ime_slike):
        self.vir = vir
        self.ime_slike = ime_slike
        