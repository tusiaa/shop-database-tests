import unittest
from assertpy import *
from parameterized import *
from unittest.mock import *
from src.klient import *

@parameterized_class(('str_wrong_value', 'int_wrong_value', 'positive_float_wrong_value'), [
    (1, "int", -5.0),
    (1.5, 1.5, "float"),
    (True, True, True),
    (None, None, None),
    ("", "", ""),
    ([1,2,3], [1,2,3], [1,2,3]),
    ({'name': 2, 'grades': 4}, {'name': 2, 'grades': 4}, {'name': 2, 'grades': 4}),
])
class TestsParametrizedKlient(unittest.TestCase):

    def setUp(self):
        def mock_znajdz_zamowienia_klienta():
            return [(1, 11)]
        def mock_czytaj_klientow():
            return [(11, "Jan", "Kowalski", "mail")]
        Baza_Danych.znajdz_klienta = Mock(return_value=(11, "Jan", "Kowalski", "mail"))
        Klient.klienci = []
        Zamowienie.zamowienia = []
        self.klient = Klient(mock_czytaj_klientow()[0][0], mock_czytaj_klientow()[0][1], mock_czytaj_klientow()[0][2], mock_czytaj_klientow()[0][3])
        zamowienie = Zamowienie(mock_znajdz_zamowienia_klienta()[0][0], mock_znajdz_zamowienia_klienta()[0][1])
        self.klient.zamowienia.append(zamowienie)

    def test_klient_init_wrong_id(self):\
        assert_that(Klient).raises(ValueError).when_called_with(self.int_wrong_value, self.klient.imie, self.klient.nazwisko, self.klient.email)

    def test_klient_init_wrong_imie(self):
        assert_that(Klient).raises(ValueError).when_called_with(self.klient.id, self.str_wrong_value, self.klient.nazwisko, self.klient.email)

    def test_klient_init_wrong_nazwisko(self):
        assert_that(Klient).raises(ValueError).when_called_with(self.klient.id, self.klient.imie, self.str_wrong_value, self.klient.email)

    def test_klient_init_wrong_email(self):
        assert_that(Klient).raises(ValueError).when_called_with(self.klient.id, self.klient.imie, self.klient.nazwisko, self.str_wrong_value)

    def test_klient_add_order_wrong_id(self):
        assert_that(self.klient.dodaj_zamowienie).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_klient_remove_order_wrong_id(self):
        assert_that(self.klient.usun_zamowienie).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_klient_change_name_wrong_name(self):
        assert_that(self.klient.zmien_imie).raises(ValueError).when_called_with(self.str_wrong_value)

    def test_klient_change_surname_wrong_surname(self):
        assert_that(self.klient.zmien_nazwisko).raises(ValueError).when_called_with(self.str_wrong_value)

    def test_klient_change_email_wrong_email(self):
        assert_that(self.klient.zmien_email).raises(ValueError).when_called_with(self.str_wrong_value)

    def test_klient_find_client_wrong_id(self):
        assert_that(Klient.znajdz_klienta).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_klient_delete_client_wrong_id(self):
        assert_that(Klient.usun_klienta).raises(ValueError).when_called_with(self.int_wrong_value)

    def tearDown(self):
        del self.klient
