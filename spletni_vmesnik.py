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
    return bottle.template(
        "osnovna_stran.html",
        t = moj_model.teme
    )

@bottle.post("/dodaj_temo/")
def dodaj_temo():
    ime = bottle.request.forms.getunicode("ime")
    tema = Tema(ime)
    moj_model.dodaj_temo(tema)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.post("/odstrani_temo/")
def odstrani_temo():
    indeks = bottle.request.forms.getunicode("indeks")
    tema = moj_model.teme[int(indeks)]
    moj_model.izbriši_temo(tema)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")



bottle.run(reloader=True,debug=True)