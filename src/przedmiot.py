from src.baza_danych import Baza_Danych

class Przedmiot:
    przedmioty = []

    def __init__(self, id: int, nazwa: str, wartosc: float):
        if type(id) is not int:
            raise ValueError("id musi być liczbą")
        if type(nazwa) is not str or not nazwa:
            raise ValueError("nazwa musi być napisem")
        if type(wartosc) is not float and type(wartosc) is not int:
            raise ValueError("wartość musi być liczbą")
        if wartosc < 0:
            raise ValueError("wartość musi być dodatnia")
        self.id = id
        self.nazwa = nazwa
        self.wartosc = float(wartosc)
        Przedmiot.przedmioty.append(self)

    def dodaj_do_bazy(self):
        Baza_Danych.dodaj_przedmiot(self.id, self.nazwa, self.wartosc)

    def usun_z_bazy(self):
        Baza_Danych.usun_przedmiot(self.id)

    def zmien_nazwe(self, nazwa):
        if type(nazwa) is not str or not nazwa:
            raise ValueError("nazwa musi być napisem")
        self.nazwa = nazwa
        Baza_Danych.edytuj_przedmiot(self.id, self.nazwa, self.wartosc)

    def zmien_wartosc(self, wartosc):
        if type(wartosc) is not float and type(wartosc) is not int:
            raise ValueError("wartość musi być liczbą")
        if wartosc < 0:
            raise ValueError("wartość musi być dodatnia")
        self.wartosc = float(wartosc)
        Baza_Danych.edytuj_przedmiot(self.id, self.nazwa, self.wartosc)

    def wszystkie_przedmioty():
        return Przedmiot.przedmioty

    def dane_wszystkie_przedmioty():
        wynik = []
        for przedmiot in Przedmiot.przedmioty:
            wynik.append((przedmiot.id, przedmiot.nazwa, przedmiot.wartosc))
        return wynik

    def znajdz_przedmiot(id):
        if type(id) is not int:
            raise ValueError("id musi być liczbą")
        for przedmiot in Przedmiot.przedmioty:
            if przedmiot.id == id:
                return przedmiot
        return None

    def usun_przedmiot(id):
        if type(id) is not int:
            raise ValueError("id musi być liczbą")
        for przedmiot in Przedmiot.przedmioty:
            if przedmiot.id == id:
                Przedmiot.przedmioty.remove(przedmiot)
                Baza_Danych.usun_przedmiot(id)
                del przedmiot
                return True
        raise ValueError("Nie ma przedmiotu o takim id")
        