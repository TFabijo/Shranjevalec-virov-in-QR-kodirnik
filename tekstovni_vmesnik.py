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

SHRANJEVALEC_VIROV = "1"
QR_KODIRNIK = "2"
IZHOD = "3"

DODAJ_TEMO = "1"
IZBRISI_TEMO = "2"
IZBERI_TEMO = "3"
NAZAJ_1 = "4"

DODAJ_VIR = "1"
IZBRISI_VIR = "2"
NAZAJ_2 = "3"

IZDELAJ_QR_KODO = "1"
NAZAJ_3 = "2"


def tekstovni_vmesnik():
    zacetni_pozdrav()
    while True:
        ukaz = izberi_moznost([
            (SHRANJEVALEC_VIROV, "sranjevalev virov"),
            (QR_KODIRNIK, "QR-kodirnk"),
            (IZHOD, "zapri program")
        ])
        if ukaz == SHRANJEVALEC_VIROV:
            pozdrav_shranjevalca()
            while True:
                prikaz_obstojecih_tem()
                izberi1 = izberi_moznost([
                    (DODAJ_TEMO,"dodaj novo temo"),
                    (IZBRISI_TEMO, "odstrani temo"),
                    (IZBERI_TEMO, "izberite temo, v kateri si zelite ogledati ali dodati vire"),
                    (NAZAJ_1,"pojdi na zacetno stran")
                ])
                if izberi1 == DODAJ_TEMO:
                    dodaj_temo()
                elif izberi1 == IZBRISI_TEMO:
                    izbrisi_temo()
                    continue
                elif izberi1 == IZBERI_TEMO:
                    print("Izberite temo, ki si jo želite ogledati ali ji dodati vire")
                    tema = izberi_temo()
                    if tema == False:
                        continue
                    else:
                        while True:
                            prikazi_obstojece_vire(tema)
                            izberi2 = izberi_moznost([
                                (DODAJ_VIR,"dodaj nov vir"),
                                (IZBRISI_VIR, "odstrani vir"),
                                (NAZAJ_2,"pojdi na stran z vsemi temami")
                            ])
                            if izberi2 == DODAJ_VIR:
                                dodaj_vir(tema)
                            elif izberi2 == IZBRISI_VIR:
                                izbrisi_vir(tema)
                            elif izberi2 == NAZAJ_2:
                                break                        
                elif izberi1 == NAZAJ_1:
                    break
        elif ukaz == QR_KODIRNIK:
            pozdrav_qr_kodirnika()
            while True:
                ukaz2 = izberi_moznost([
                    (IZDELAJ_QR_KODO,"izdelaj qr-kodo"),
                    (NAZAJ_3,"pojdi na zaćetno stran")
                ])
                if ukaz2 == IZDELAJ_QR_KODO:
                    sprejem_podatkov_za_izdelavo_kode()
                elif ukaz2 == NAZAJ_3:
                    break
        elif ukaz == IZHOD:
            moj_model.shrani_v_datoteko(IME_DATOTEKE)
            print("Nasvidenje")
            break

###############OSNOVNE FUNKCIJE#################
def pozdrav_qr_kodirnika():
    print("QR-kodirnik")
def sprejem_podatkov_za_izdelavo_kode():
    vir = input("vir,kateremu zelite izdelati QR-kodo:")
    ime_slike = input("poimenujte sliko QR-kode:")
    nova_koda = QR_kodirnik(vir,ime_slike)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    qr.add_data(f"{nova_koda.vir}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{nova_koda.ime_slike}.png")
    if img == error:
        print("NAPAKA! izdelava QR-kode ni uspela")
    else:
        print("QR-koda je uspešno izdelana")
        print("slika kode je na vašem računaliku")

def zacetni_pozdrav():
    print("Lepo pozdravljeni")

def pozdrav_shranjevalca():
    print("Shranjevalec virov")

def prikaz_obstojecih_tem():
    if len(moj_model.teme) >= 1:
        print("Teme:")
        for t in moj_model.teme:
            print(f"-{t.ime}")
    else:
        print("Trenuto ni nobene teme, zato morate ustvariti eno")
        dodaj_temo()

def dodaj_temo():
    print("Vnesite ime teme")
    while True:
        print("Če nočete vstaviti nove teme, vstavite /")
        ime = input("Ime: ")
        nova_tema = Tema(ime)
        if ime == "/":
            break
        elif f"{nova_tema.ime}".lower() in [f"{tema.ime}".lower() for tema in moj_model.teme]:
            print("Ta tema že obstaja, prosim izberite drugo")
        else:
            moj_model.dodaj_temo(nova_tema)
            break

def izbrisi_temo():
    tema = prikazi_temo(moj_model)
    if tema == 0:
        return 0
    else:
        moj_model.izbriši_temo(tema)

def izberi_temo():
    print("0) nazaj ")
    for i,tema in enumerate(moj_model.teme,1):
        print(f"{i}) {tema.ime}")
    while True:
        i = preberi_stevilo()
        if i == 0:
            return False
        if 1 <= i <= len(moj_model.teme):
            moznost = moj_model.teme[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moj_model.teme)}.")

def prikazi_obstojece_vire(tema):
    if len(tema.viri) < 1:
        print("ta tema še nima nobenega vira")
    else:
        for vir in (tema.viri):
            print(f"-vir:{vir.ime}")
            print(f" opis:{vir.opis}")
            print(f" dodano:{vir.datum}")

def dodaj_vir(tema):
    print("Vnesite vir")
    while True:
        print("Če nočete vstaviti novega vira, pri viru vstavite /")
        vir = input("vir: ")
        opis = input("Opis vira: ")
        nov_vir = Viri(vir,opis)
        if vir == "/":
            break
        elif nov_vir.ime in [v.ime for v in tema.viri]:
            print("Ta vir že obstaja")
            for v in tema.viri:
                if v.ime == vir:
                    print(f"dodan: {v.datum}")
                    print(f"z opisom: {v.opis}")
        else:
            tema.dodaj_vir(nov_vir)
            break

def izbrisi_vir(tema):
    if len(tema.viri) == 0:
        print("v teji temi še ni virov")
    else:
        vir = prikazi_vir(tema)
        if vir == False:
            return 0
        else:
            tema.odstrani_vir(vir)

######################## POMOŽNE FUKCIJE OSNOVIH FUNKCJI ##############
def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")

def izberi_moznost(seznam_moznosti):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    for i, (_moznost, opis) in enumerate(seznam_moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(seznam_moznosti):
            moznost, _opis = seznam_moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(seznam_moznosti)}.")

def prikazi_temo(model):
    print("0) nocem izbrisati nobene teme")
    for i,tema in enumerate(model.teme,1):
        print(f"{i}) {tema.ime}")
    while True:
        i = preberi_stevilo()
        if i == 0:
            return 0
        elif 1 <= i <= len(model.teme):
            moznost = model.teme[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(model.teme)}.")

def prikazi_vir(tema):
    print("0) nocem izbrisati nobenega vira")
    for i,vir in enumerate(tema.viri,1):
        print(f"{i})vir: {vir.ime}")
        print(f"    opis: {vir.opis}")
        print(f"    datum: {vir.datum}")
    while True:
        i = preberi_stevilo()
        if i == 0:
            return False
        elif 1 <= i <= len(tema.viri):
            moznost = tema.viri[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(tema.viri)}.")


tekstovni_vmesnik()





    

