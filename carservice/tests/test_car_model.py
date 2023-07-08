from datetime import timedelta

from django.utils.timezone import now
from django.test import TestCase
from carservice.models import Car, Offer, Rent


class TestCar(TestCase):
    def test_string_method(self):
        car = Car(car_model='Astra', car_brand='Opel', vin='12345678901234567', car_mileage=123456, date_of_prod=2010)
        self.assertEqual(str(car), 'Model: Astra Opel, vin number: (12345678901234567)')


class TestOffer(TestCase):
    def test_string_method(self):
        car = Car(car_model='Astra', car_brand='Opel')
        offer = Offer(price=100.0, car=car)
        self.assertEqual(str(offer), 'Price: (100.0), car:(Astra Opel)')


class TestRent(TestCase):
    def test_save_method(self):
        car = Car()



