import json
from src.baza_danych import Baza_Danych
from src.zamowienie import *

class Klient:
    klienci = []

    def __init__(self, id, imie, nazwisko, email):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        if type(imie) is not str or not imie:
            raise ValueError("imie nie jest stringiem")
        if type(nazwisko) is not str or not nazwisko:
            raise ValueError("nazwisko nie jest stringiem")
        if type(email) is not str or not email:
            raise ValueError("email nie jest stringiem")
        if Klient.znajdz_klienta(id):
            raise ValueError("klient o takim id juz istnieje")
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.zamowienia = []
        Klient.klienci.append(self)

    def dodaj_zamowienie(self, id):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        self.zamowienia.append(Zamowienie(id, self.id))
        Baza_Danych.dodaj_zamowienie(id, self.id)

    def usun_zamowienie(self, id):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        self.zamowienia.remove(Zamowienie.znajdz_zamowienie(id))
        Zamowienie.usun_zamowienie(id)

    def zmien_imie(self, imie):
        if type(imie) is not str or not imie:
            raise ValueError("imie nie jest stringiem")
        self.imie = imie
        Baza_Danych.edytuj_klienta(self.id, self.imie, self.nazwisko, self.email)

    def zmien_nazwisko(self, nazwisko):
        if type(nazwisko) is not str or not nazwisko:
            raise ValueError("nazwisko nie jest stringiem")
        self.nazwisko = nazwisko
        Baza_Danych.edytuj_klienta(self.id, self.imie, self.nazwisko, self.email)

    def zmien_email(self, email):
        if type(email) is not str or not email:
            raise ValueError("email nie jest stringiem")
        self.email = email
        Baza_Danych.edytuj_klienta(self.id, self.imie, self.nazwisko, self.email)

    def dane_zamowienia(self):
        wynik = []
        for zamowienie in self.zamowienia:
            przedmioty = []
            id = Baza_Danych.znajdz_przedmioty_z_zamowienia(zamowienie.id)
            for przedmiot in id:
                item = Baza_Danych.znajdz_przedmiot(przedmiot[1])
                przedmioty.append(item)
            wynik.append(przedmioty)
        return wynik

    def wszyscy_klienci():
        return Klient.klienci

    def dane_wszyscy_klienci():
        wynik = []
        for klient in Klient.klienci:
            wynik.append((klient.id, klient.imie, klient.nazwisko, klient.email))
        return wynik

    def znajdz_klienta(id):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        for klient in Klient.klienci:
            if klient.id == id:
                return klient
        return None

    def usun_klienta(id):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        for klient in Klient.klienci:
            if klient.id == id:
                Klient.klienci.remove(klient)
                del klient
                Baza_Danych.usun_klienta(id)
                return True
        raise ValueError("Nie ma takiego klienta")

    def zapisz_do_pliku():
        with open("data/klienci.json", "w") as plik:
            wynik = []
            for klient in Klient.klienci:
                wynik.append(klient)
            plik.write(json.dumps(wynik, indent=4, default=vars))
        