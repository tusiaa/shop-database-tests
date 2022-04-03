import unittest
from assertpy import *
from parameterized import *
from unittest.mock import *
from src.zamowienie import *

@parameterized_class(('str_wrong_value', 'int_wrong_value', 'positive_float_wrong_value'), [
    (1, "int", -5.0),
    (1.5, 1.5, "float"),
    (True, True, True),
    (None, None, None),
    ("", "", ""),
    ([1,2,3], [1,2,3], [1,2,3]),
    ({'name': 2, 'grades': 4}, {'name': 2, 'grades': 4}, {'name': 2, 'grades': 4}),
])
class TestsParametrizedZamowienie(unittest.TestCase):

    def setUp(self):
        def mock_czytaj_zamowienia():
            return [(1, 11)]
        def mock_znajdz_przedmiot():
            return (111, "Nazwa", 100.0)
        Baza_Danych.znajdz_klienta = Mock(return_value=(11, "Jan", "Kowalski", "mail"))
        Zamowienie.zamowienia = []
        self.zamowienie = Zamowienie(mock_czytaj_zamowienia()[0][0], mock_czytaj_zamowienia()[0][1])
        przedmiot = Przedmiot(mock_znajdz_przedmiot()[0], mock_znajdz_przedmiot()[1], mock_znajdz_przedmiot()[2])
        self.zamowienie.przedmioty.append(przedmiot)

    def test_zamowienie_init_wrong_id(self):
        assert_that(Zamowienie).raises(ValueError).when_called_with(self.int_wrong_value, self.zamowienie.klient_id)

    def test_zamowienie_init_wrong_klient_id(self):
        assert_that(Zamowienie).raises(ValueError).when_called_with(self.zamowienie.id, self.int_wrong_value)

    def test_zamowienie_add_item_wrong_id(self):
        assert_that(self.zamowienie.dodaj_przedmiot).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_zamowienie_remove_item_wrong_id(self):
        assert_that(self.zamowienie.usun_przedmiot).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_zamowienie_check_if_item_in_order_wrong_id(self):
        assert_that(self.zamowienie.czy_jest_przedmiot).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_zamowienie_find_order_wrong_id(self):
        assert_that(Zamowienie.znajdz_zamowienie).raises(ValueError).when_called_with(self.int_wrong_value)

    def test_zamowienie_delete_order_wrong_id(self):
        assert_that(Zamowienie.usun_zamowienie).raises(ValueError).when_called_with(self.int_wrong_value)

    def tearDown(self):
        del self.zamowienie
