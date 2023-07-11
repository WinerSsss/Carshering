from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth.models import User

from carservice import forms
from carservice.models import Rent


class TestCarUpdateForm(TestCase):
    def test_car_update_form(self):
        form = forms.CarUpdateForm(data={
            'vin': '1G8MG35X48Y106575',
            'car_mileage': 123456,
            'car_brand': 'Opel',
            'car_model': 'Astra',
            'date_of_prod': 2010
            })
        self.assertTrue(form.is_valid())


class TestOfferUpdateForm(TestCase):
    def test_offer_update_form(self):
        form = forms.OfferUpdateForm(data={
            'description': 'test description',
            'price': 100.0
            })
        self.assertTrue(form.is_valid())


class TestRentUpdateForm(TestCase):
    def test_rent_update_form(self):
        form = forms.RentUpdateForm(data={
            'rent_start': now().date(),
            'duration': 10
            })
        self.assertTrue(form.is_valid())


class TestRentDeleteForm(TestCase):
    def test_rent_delete_form(self):
        user = User.objects.create(username='testuser', password='12345')
        rent_queryset = Rent.objects.filter(user=user)
        form = forms.RentDeleteForm(user=user)
        self.assertEqual(form.fields['rent'].queryset.count(), rent_queryset.count())
        self.assertQuerySetEqual(form.fields['rent'].queryset, rent_queryset, transform=lambda x: x)
