import unittest
from assertpy import *
from unittest.mock import *
from src.przedmiot import *

class TestsPrzedmiot(unittest.TestCase):

    def setUp(self):
        def mock_czytaj_przedmioty():
            return [(1, "Nazwa", 100.0)]
        Przedmiot.przedmioty = []
        self.przedmiot = Przedmiot(mock_czytaj_przedmioty()[0][0], mock_czytaj_przedmioty()[0][1], mock_czytaj_przedmioty()[0][2])

    def test_przedmiot_init(self):
        assert_that(self.przedmiot).is_not_none()

    @patch.object(Baza_Danych, 'dodaj_przedmiot')
    def test_przedmiot_add_item_to_database(self, mock_dodaj_przedmiot):
        self.przedmiot.dodaj_do_bazy()
        mock_dodaj_przedmiot.assert_called_once_with(self.przedmiot.id, self.przedmiot.nazwa, self.przedmiot.wartosc)

    @patch.object(Baza_Danych, 'dodaj_przedmiot', side_effect=[None, ValueError])
    def test_przedmiot_add_item_to_database_already_exists(self, mock_dodaj_przedmiot):
        self.przedmiot.dodaj_do_bazy()
        assert_that(self.przedmiot.dodaj_do_bazy).raises(ValueError)

    @patch.object(Baza_Danych, 'usun_przedmiot')
    def test_przedmiot_delete_item_from_database(self, mock_usun_przedmiot):
        self.przedmiot.usun_z_bazy()
        mock_usun_przedmiot.assert_called_once_with(self.przedmiot.id)

    @patch.object(Baza_Danych, 'usun_przedmiot', side_effect=[None, ValueError])
    def test_przedmiot_delete_item_from_database_not_exists(self, mock_usun_przedmiot):
        self.przedmiot.usun_z_bazy()
        assert_that(self.przedmiot.usun_z_bazy).raises(ValueError)

    @patch.object(Baza_Danych, 'edytuj_przedmiot')
    def test_przedmiot_change_name(self, mock_edytuj_przedmiot):
        self.przedmiot.zmien_nazwe("Nowa nazwa")
        mock_edytuj_przedmiot.assert_called_once_with(self.przedmiot.id, "Nowa nazwa", self.przedmiot.wartosc)

    @patch.object(Baza_Danych, 'edytuj_przedmiot')
    def test_przedmiot_change_value_float(self, mock_edytuj_przedmiot):
        self.przedmiot.zmien_wartosc(200.99)
        mock_edytuj_przedmiot.assert_called_once_with(self.przedmiot.id, self.przedmiot.nazwa, 200.99)

    @patch.object(Baza_Danych, 'edytuj_przedmiot')
    def test_przedmiot_change_value_int(self, mock_edytuj_przedmiot):
        self.przedmiot.zmien_wartosc(200)
        mock_edytuj_przedmiot.assert_called_once_with(self.przedmiot.id, self.przedmiot.nazwa, float(200))

    def test_przedmiot_get_items(self):
        assert_that(Przedmiot.wszystkie_przedmioty()).contains(self.przedmiot)

    def test_przedmiot_get_items_empty(self):
        Przedmiot.przedmioty = []
        assert_that(Przedmiot.wszystkie_przedmioty()).is_empty()

    def test_przedmiot_get_data_items(self):
        assert_that(Przedmiot.dane_wszystkie_przedmioty()).contains((self.przedmiot.id, self.przedmiot.nazwa, self.przedmiot.wartosc))

    def test_przedmiot_get_data_items_empty(self):
        Przedmiot.przedmioty = []
        assert_that(Przedmiot.dane_wszystkie_przedmioty()).is_empty()

    def test_przedmiot_find_item(self):
        assert_that(Przedmiot.znajdz_przedmiot(self.przedmiot.id)).is_equal_to(self.przedmiot)

    def test_przedmiot_find_item_not_found(self):
        assert_that(Przedmiot.znajdz_przedmiot(112)).is_none()

    @patch.object(Baza_Danych, 'usun_przedmiot')
    def test_przedmiot_delete_item(self, mock_usun_przedmiot):
        Przedmiot.usun_przedmiot(self.przedmiot.id)
        assert_that(Przedmiot.przedmioty).is_empty()

    @patch.object(Baza_Danych, 'usun_przedmiot')
    def test_przedmiot_delete_item_database_check(self, mock_usun_przedmiot):
        Przedmiot.usun_przedmiot(self.przedmiot.id)
        mock_usun_przedmiot.assert_called_once_with(self.przedmiot.id)

    @patch.object(Baza_Danych, 'usun_przedmiot')
    def test_przedmiot_delete_item_not_found(self, mock_usun_przedmiot):
        assert_that(Przedmiot.usun_przedmiot).raises(ValueError).when_called_with(112)
    
    def tearDown(self):
        del self.przedmiot
