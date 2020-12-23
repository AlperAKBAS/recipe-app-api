from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError

from django.test import TestCase

class CommandTests(TestCase):

    # test what happens when we call our command and the database is already available
    # yazacağımız bekleme komutu çalışıyor mu?
    def test_wait_for_db_ready(self):
        """ Test waiting for db when db is available """
        #simulate django when db available
        print('___Testing as if database available.')
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi: #bu modülü mock ediyoruz
            gi.return_value = True # sanki db yüklenmiş gibi 
            call_command('wait_for_db') # the command we create
            self.assertEqual(gi.call_count, 1) # bir kere mi çağrıldı
    
    # Gerçekten db yüklenmeden bekliyor mu? bunun için önce db fail etti gibi bir case simule etmemiz lazım
    @patch('time.sleep', return_value=True) # test aşamasında 5 saniye beklememize gerek yok.
    def test_wait_for_db(self, ts): #gi yı arg olarak pass ediyor
        """Test waiting for db""" 
        print('___Testing database not available for 5 trials.')
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True] # beş kez OE ver altıncısında True ve bakalım ne olacak
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

