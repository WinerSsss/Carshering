from datetime import timedelta

from django.utils.timezone import now
from django.test import TestCase
from django.contrib.auth.models import User

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
    def test_string_method(self):
        status = Rent.ACTIVE
        duration = 10
        user = User(username='testuser', password='12345')
        car = Car(car_model='Astra', car_brand='Opel')
        offer = Offer(price=100.0, car=car, user=user)
        rent = Rent(status=status, duration=duration, offer=offer, user=user)
        self.assertEqual(str(rent), f'Rent status: {status}, rent duration: ({duration}), offer: {offer}, user: {user}')


class TestRentSaveMethod(TestCase):
    def test_save_method(self):
        user = User.objects.create(username='testuser', password='12345')
        car = Car.objects.create(car_model='Astra', car_brand='Opel', car_mileage=100000, user=user)
        offer = Offer.objects.create(price=100.0, car=car, user=user)
        rent = Rent.objects.create(offer=offer, user=user, duration=10, rent_start=now().date())
        rent.save()
        self.assertEqual(rent.status, Rent.ACTIVE)
        rent = Rent.objects.create(offer=offer, user=user, duration=10, rent_start=now().date() + timedelta(days=10))
        rent.save()
        self.assertEqual(rent.status, Rent.PENDING)
        rent = Rent.objects.create(offer=offer, user=user, duration=10, rent_start=now().date())
        rent.close_rent = True
        rent.save()
        self.assertEqual(rent.status, rent.FINISHED)
        rent = Rent.objects.create(offer=offer, user=user, duration=10, rent_start=now().date())
        rent.rent_end = rent.rent_start + timedelta(days=10)
        rent.save()
        self.assertEqual(rent.rent_start + timedelta(days=10), rent.rent_end)
