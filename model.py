from datetime import date
import datetime
import json


def zasifriraj_geslo(geslo_v_cistopisu):
    zasifrirano_geslo = "xxx" + geslo_v_cistopisu[::-1] + "xxx"
    return zasifrirano_geslo

class Uporabnik:
    def __init__(self,uporabnisko_ime,zasifrirano_geslo,model):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.model = model

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Model())
            uporabnik.v_datoteko()
            return uporabnik

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "model": self.model.v_slovar()
        }

    def v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime),"w") as datoteka:
            json.dump(self.v_slovar(),datoteka,ensure_ascii=False, indent=4)

    def preveri_geslo(self,geslo_v_cistopisu):
        return self.zasifrirano_geslo == zasifriraj_geslo(geslo_v_cistopisu)

    def nastavi_geslo(self,geslo_v_cistopisu):
        self.zasifrirano_geslo = zasifriraj_geslo(geslo_v_cistopisu)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        geslo = slovar["zasifrirano_geslo"]
        model = Model.iz_slovarja(slovar["model"])
        return Uporabnik(uporabnisko_ime,geslo,model)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

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

    def preveri_podatke_nove_teme(self, ime):
        napaka = {}
        if not ime:
            napaka["ime"] = "tema mora biti neprazna."
        for t in self.teme:
            if t.ime == ime:
                napaka["ime"] = "tema že obstaja."
        return napaka
    
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

    def preveri_podatke_novega_vira(self, vir):
        napake = {}
        if not vir:
            napake["vir"] = "vir mora biti neprazen."
        for v in self.viri:
            if v.ime == vir:
                napake["vir"] = "vir že obstaja."
        return napake

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
        