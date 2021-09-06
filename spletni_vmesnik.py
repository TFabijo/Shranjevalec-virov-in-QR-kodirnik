from re import template
import bottle
from os import error, path
from model import Model
from model import Tema
from model import Viri
from model import QR_kodirnik
from model import Uporabnik
import qrcode

IME_DATOTEKE = "stanje.json"
PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to bo pa tezko"



def shrani_stanje(uporabnik):
    uporabnik.shrani_stanje()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)         
    else:
        bottle.redirect("/prijava/")

def podatki_uporabnika(uporabnisko_ime):
    try:
        return Uporabnik.iz_datoteke(uporabnisko_ime)
    except FileNotFoundError:
        bottle.redirect("prijava/")
            

@bottle.get("/")
def zacetna_stran():
    bottle.redirect("/osnovna_stran/")


@bottle.get("/osnovna_stran/")
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template("domaca.html",uporabnik=uporabnik)

@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
        )
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template(
            "registracija.html", napaka=e.args[0]
        )

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka = None)



@bottle.post("/prijava/")
def prijava_post():
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    uporabnisko = bottle.request.forms.getunicode("uporabnisko_ime")
    if uporabnisko:
        uporabnik = podatki_uporabnika(uporabnisko)
        if uporabnik.preveri_geslo(geslo_v_cistopisu):
            bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko, path="/", secret=SKRIVNOST)
            bottle.redirect("/")
        else:
           return bottle.template("prijava.html", napaka = "Podatki za prijavo so napačni!") 
    else:
        return bottle.template("prijava.html", napaka = "Vnesi uporabniško ime")

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")        

@bottle.get("/prikazi_teme/")
def prikazi_teme():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "teme.html",
        t = uporabnik.model.teme,
        u = uporabnik.uporabnisko_ime,
        polja = {},
        napaka = {}
    )


@bottle.post("/dodaj_temo/")
def dodaj_temo():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime":ime}
    napaka = uporabnik.model.preveri_podatke_nove_teme(ime)
    if napaka:
        return bottle.template("teme.html", t = uporabnik.model.teme, napaka=napaka, polja=polja, u = uporabnik.uporabnisko_ime)
    else:
        tema = Tema(ime)
        uporabnik.model.dodaj_temo(tema)
        uporabnik.v_datoteko()
        bottle.redirect("/prikazi_teme/")

@bottle.post("/odstrani_temo/")
def odstrani_temo():
    uporabnik = trenutni_uporabnik()
    indeks = bottle.request.forms.getunicode("indeks")
    tema = uporabnik.model.teme[int(indeks)]
    uporabnik.model.izbriši_temo(tema)
    uporabnik.v_datoteko()
    bottle.redirect("/prikazi_teme/")

@bottle.get("/poglej_vire/")
def poglej_vire():
    uporabnik = trenutni_uporabnik()
    indeks = bottle.request.query.getunicode("indeks")
    tema = uporabnik.model.teme[int(indeks)]
    return bottle.template(
        "viri_teme.html",
        i = indeks,
        ime = str(tema.ime).capitalize(),
        t = tema,
        viri = tema.viri,
        u = uporabnik.uporabnisko_ime
    )


@bottle.get("/obrazec_za_dodajanje_vira/")
def obrazec_za_dodajanje_vira():

    uporabnik = trenutni_uporabnik()
    indeks_teme = bottle.request.query.getunicode("tema")
    tema = uporabnik.model.teme[int(indeks_teme)]
    return bottle.template(
        "obrazec_za_dodajanje_vira.html",
        napake = {} ,
        polja = {},
        ime = str(tema.ime).capitalize(),
        i = indeks_teme,
        t = tema,
        u = uporabnik.uporabnisko_ime 
    )

@bottle.post("/dodaj_vir/")
def dodaj_vir():
    uporabnik = trenutni_uporabnik()
    indeks_teme = bottle.request.forms.getunicode("indeks_teme")
    vir = bottle.request.forms.getunicode("vir")
    opis = bottle.request.forms.getunicode("opis")
    polja = {"vir": vir}
    tema = uporabnik.model.teme[int(indeks_teme)]
    napake = tema.preveri_podatke_novega_vira(vir)
    if napake:
        return bottle.template("obrazec_za_dodajanje_vira.html", napake=napake, polja=polja,ime = str(tema.ime).capitalize(),
        i = indeks_teme,
        t = tema, u = uporabnik.uporabnisko_ime)
    else:
        v = Viri(vir,opis)
        tema.dodaj_vir(v)
        uporabnik.v_datoteko()
        bottle.redirect(f"/poglej_vire/?indeks={indeks_teme}")


@bottle.post("/odstrani_vir/")
def odstrani_vir():
    uporabnik = trenutni_uporabnik()
    indeks_teme = bottle.request.forms.getunicode("tema")
    indeks =  bottle.request.forms.getunicode("indeks")
    tema = uporabnik.model.teme[int(indeks_teme)]
    tema.odstrani_vir(tema.viri[int(indeks)])
    uporabnik.v_datoteko()
    bottle.redirect(f"/poglej_vire/?indeks={indeks_teme}")

#@bottle.post("/dodaj_vir/")
#def dodaj_vir():
    #indeks_teme = bottle.request.forms.getunicode("tema")
    #ime = bottle.request.forms.getunicode("ime")
    #opis = bottle.request.forms.getunicode("opis")
    #vir = Viri(ime,opis)
    #moj_model.teme[int(indeks_teme)].dodaj_vir(vir)
    #moj_model.shrani_v_datoteko(IME_DATOTEKE)
    #bottle.redirect(f"/poglej_vire/?indeks={indeks_teme}")

@bottle.get("/qr_kodirnik/")
def zavetna_qr_kodirnik():
    trenutni_uporabnik()
    return bottle.template(
        "QR-kodirnik.html"
    )

@bottle.post("/izdelaj_QR/")
def izdelaj_QR():
    vir = bottle.request.forms.getunicode("vir")
    ime_slike = bottle.request.forms.getunicode("ime")
    nova_koda = QR_kodirnik(vir,ime_slike)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    slika_ime = str(nova_koda.ime_slike).replace(" ", "_")
    qr.add_data(f"{nova_koda.vir}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{slika_ime}.png")
    return bottle.template(
        "koda.html",
        s = f"{ime_slike}.png"
    )

@bottle.error(404)
def error_404(error):
    return bottle.template("napaka.html")
 






bottle.run(reloader=True,debug=True)