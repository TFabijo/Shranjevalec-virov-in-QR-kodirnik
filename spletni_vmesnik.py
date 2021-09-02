import bottle
from os import error
from model import Model
from model import Tema
from model import Viri
from model import QR_kodirnik
import qrcode

IME_DATOTEKE = "stanje.json"
try:
    moj_model = Model.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Model()


@bottle.get("/")
def osnovna_stran():
    return bottle.template("domaca.html")

@bottle.get("/prikazi_teme/")
def prikazi_teme():
    return bottle.template(
        "teme.html",
        t = moj_model.teme
    )


@bottle.post("/dodaj_temo/")
def dodaj_temo():
    ime = bottle.request.forms.getunicode("ime")
    tema = Tema(ime)
    moj_model.dodaj_temo(tema)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/prikazi_teme/")

@bottle.post("/odstrani_temo/")
def odstrani_temo():
    indeks = bottle.request.forms.getunicode("indeks")
    tema = moj_model.teme[int(indeks)]
    moj_model.izbriši_temo(tema)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.get("/poglej_vire/")
def poglej_vire():
    indeks = bottle.request.query.getunicode("indeks")
    tema = moj_model.teme[int(indeks)]
    return bottle.template(
        "viri_teme.html",
        i = indeks,
        t = tema,
        viri = tema.viri
    )
@bottle.post("/odstrani_vir/")
def odstrani_vir():
    indeks_teme = bottle.request.forms.getunicode("tema")
    indeks =  bottle.request.forms.getunicode("indeks")
    tema = moj_model.teme[int(indeks_teme)]
    tema.odstrani_vir(tema.viri[int(indeks)])
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect(f"/poglej_vire/?indeks={indeks_teme}")

@bottle.post("/dodaj_vir/")
def dodaj_vir():
    indeks_teme = bottle.request.forms.getunicode("tema")
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    vir = Viri(ime,opis)
    moj_model.teme[int(indeks_teme)].dodaj_vir(vir)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect(f"/poglej_vire/?indeks={indeks_teme}")
    




bottle.run(reloader=True,debug=True)