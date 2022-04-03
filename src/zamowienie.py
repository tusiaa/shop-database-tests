from src.baza_danych import Baza_Danych
from src.przedmiot import Przedmiot

class Zamowienie:
    zamowienia = []

    def __init__(self, id: int, klient_id: int):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        if type(klient_id) is not int:
            raise ValueError("klient_id nie jest liczba")
        if not Baza_Danych.znajdz_klienta(klient_id):
            raise ValueError("Nie ma takiego klienta")
        self.id = id
        self.klient_id = klient_id
        self.przedmioty = []
        Zamowienie.zamowienia.append(self)

    def dodaj_przedmiot(self, przedmiot_id: int):
        if type(przedmiot_id) is not int:
            raise ValueError("przedmiot_id nie jest liczba")
        if not Baza_Danych.znajdz_przedmiot(przedmiot_id):
            raise ValueError("Nie ma takiego przedmiotu")
        for przedmiot in Przedmiot.przedmioty:
            if przedmiot.id == przedmiot_id:
                self.przedmioty.append(przedmiot)
                Baza_Danych.dodaj_przedmiot_do_zamowienia(self.id, przedmiot_id)

    def usun_przedmiot(self, przedmiot_id: int):
        if type(przedmiot_id) is not int:
            raise ValueError("przedmiot_id nie jest liczba")
        for przedmiot in self.przedmioty:
            if przedmiot.id == przedmiot_id:
                self.przedmioty.remove(przedmiot)
                Baza_Danych.usun_przedmiot_z_zamowienia(self.id, przedmiot_id)
                return True
        raise ValueError("Nie ma takiego przedmiotu")

    def czy_jest_przedmiot(self, przedmiot_id: int):
        if type(przedmiot_id) is not int:
            raise ValueError("przedmiot_id nie jest liczba")
        for przedmiot in self.przedmioty:
            if przedmiot.id == przedmiot_id:
                return True
        return False

    def dane_klient(self):
        return Baza_Danych.znajdz_klienta(self.klient_id)

    def dane_przedmioty(self):
        wynik = []
        for przedmiot in self.przedmioty:
            wynik.append((przedmiot.id, przedmiot.nazwa, przedmiot.wartosc))
        return wynik

    def wszystkie_zamowienia():
        return Zamowienie.zamowienia

    def znajdz_zamowienie(id: int):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        for zamowienie in Zamowienie.zamowienia:
            if zamowienie.id == id:
                return zamowienie
        return None

    def usun_zamowienie(id: int):
        if type(id) is not int:
            raise ValueError("id nie jest liczba")
        for zamowienie in Zamowienie.zamowienia:
            if zamowienie.id == id:
                Zamowienie.zamowienia.remove(zamowienie)
                Baza_Danych.usun_zamowienie(id)
                del zamowienie
                return True
        raise ValueError("Nie ma takiego zamowienia")
