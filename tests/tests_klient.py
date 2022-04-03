import unittest
from assertpy import *
from unittest.mock import *
from src.klient import *

class TestsKlient(unittest.TestCase):

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

    def test_klient_init(self):
        assert_that(self.klient).is_not_none()

    def test_klient_add_order(self,):
        self.klient.dodaj_zamowienie(2)
        assert_that(self.klient.zamowienia).is_length(2)

    @patch.object(Baza_Danych, 'dodaj_zamowienie')
    def test_klient_add_order_database_check(self, mock_dodaj_zamowienie):
        self.klient.dodaj_zamowienie(2)
        mock_dodaj_zamowienie.assert_called_with(2, self.klient.id)

    def test_klient_remove_order(self):
        zamowienie = self.klient.zamowienia[0]
        self.klient.usun_zamowienie(1)
        assert_that(self.klient.zamowienia).does_not_contain(zamowienie)

    @patch.object(Baza_Danych, 'usun_zamowienie', autospec=True)
    def test_klient_remove_order_database_check(self, mock_usun_zamowienie):
        self.klient.usun_zamowienie(1)
        mock_usun_zamowienie.assert_called_with(1)

    @patch.object(Baza_Danych, 'usun_zamowienie', autospec=True)
    def test_klient_remove_order_order_check(self, mock_usun_zamowienie):
        zamowienie = self.klient.zamowienia[0]
        self.klient.usun_zamowienie(1)
        assert_that(Zamowienie.zamowienia).does_not_contain(zamowienie)

    def test_klient_remove_order_not_found(self):
        assert_that(self.klient.usun_zamowienie).raises(ValueError).when_called_with(2)

    def test_klient_change_name(self):
        self.klient.zmien_imie("Janusz")
        assert_that(self.klient.imie).is_equal_to("Janusz")

    def test_klient_change_surname(self):
        self.klient.zmien_nazwisko("Nowak")
        assert_that(self.klient.nazwisko).is_equal_to("Nowak")

    def test_klient_change_email(self):
        self.klient.zmien_email("test.email")
        assert_that(self.klient.email).is_equal_to("test.email")

    @patch.object(Baza_Danych, 'edytuj_klienta', autospec=True)
    def test_klient_change_name_database_check(self, mock_edytuj_klienta):
        self.klient.zmien_imie("Janusz")
        mock_edytuj_klienta.assert_called_with(self.klient.id, "Janusz", self.klient.nazwisko, self.klient.email)

    @patch.object(Baza_Danych, 'edytuj_klienta', autospec=True)
    def test_klient_change_surname_database_check(self, mock_edytuj_klienta):
        self.klient.zmien_nazwisko("Nowak")
        mock_edytuj_klienta.assert_called_with(self.klient.id, self.klient.imie, "Nowak", self.klient.email)

    @patch.object(Baza_Danych, 'edytuj_klienta', autospec=True)
    def test_klient_change_email_database_check(self, mock_edytuj_klienta):
        self.klient.zmien_email("test.email")
        mock_edytuj_klienta.assert_called_with(self.klient.id, self.klient.imie, self.klient.nazwisko, "test.email")

    @patch.object(Baza_Danych, 'znajdz_przedmioty_z_zamowienia', return_value=[(1, 111), (1, 222)], autospec=True)
    @patch.object(Baza_Danych, 'znajdz_przedmiot', side_effect=[(111, "Nazwa", 100.0), (222, "Nazwa2", 200.0)], autospec=True)
    def test_klient_get_orders(self, mock_znajdz_przedmiot, mock_znajdz_zamowienie):
        assert_that(self.klient.dane_zamowienia()).contains([(111, "Nazwa", 100.0), (222, "Nazwa2", 200.0)])
        
    @patch.object(Baza_Danych, 'znajdz_przedmioty_z_zamowienia', return_value=[(1, 111), (1, 222)], autospec=True)
    @patch.object(Baza_Danych, 'znajdz_przedmiot', side_effect=[(111, "Nazwa", 100.0), (222, "Nazwa2", 200.0)], autospec=True)
    def test_klient_get_orders_database_check(self, mock_znajdz_przedmiot, mock_znajdz_zamowienie):
        self.klient.dane_zamowienia()
        mock_znajdz_zamowienie.assert_called_with(1)

    def test_klient_get_orders_empty(self):
        self.klient.zamowienia = []
        assert_that(self.klient.dane_zamowienia()).is_empty()

    def test_klient_get_clients(self):
        assert_that(Klient.wszyscy_klienci()).contains(self.klient)

    def test_klient_get_clients_empty(self):
        Klient.klienci = []
        assert_that(Klient.wszyscy_klienci()).is_empty()

    def test_klient_get_data_clients(self):
        assert_that(Klient.dane_wszyscy_klienci()).contains((self.klient.id, self.klient.imie, self.klient.nazwisko, self.klient.email))

    def test_klient_get_data_clients_empty(self):
        Klient.klienci = []
        assert_that(Klient.dane_wszyscy_klienci()).is_empty()

    def test_klient_find_by_id(self):
        assert_that(Klient.znajdz_klienta(11)).is_equal_to(self.klient)

    def test_klient_find_by_id_not_found(self):
        assert_that(Klient.znajdz_klienta(12)).is_none()

    @patch.object(Baza_Danych, 'usun_klienta', autospec=True)
    def test_klient_delete_by_id(self, mock_usun_klienta):
        Klient.usun_klienta(self.klient.id)
        assert_that(Klient.wszyscy_klienci()).does_not_contain(self.klient)

    @patch.object(Baza_Danych, 'usun_klienta', autospec=True)
    def test_klient_delete_by_id_database_check(self, mock_usun_klienta):
        Klient.usun_klienta(self.klient.id)
        mock_usun_klienta.assert_called_with(self.klient.id)

    def test_klient_delete_by_id_not_found(self):
        assert_that(Klient.usun_klienta).raises(ValueError).when_called_with(12)

    def test_klient_save_to_file(self):
        mock = mock_open()
        with patch('builtins.open', mock):
            Klient.zapisz_do_pliku()
        mock.assert_called_with('data/klienci.json', 'w')

    def test_klient_save_to_file_write_check(self):
        mock = mock_open()
        with patch('builtins.open', mock):
            Klient.zapisz_do_pliku()
        mock.return_value.write.assert_called_with(json.dumps([self.klient], indent=4, default=vars))

    def tearDown(self):
        del self.klient