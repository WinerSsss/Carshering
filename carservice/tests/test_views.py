import datetime

from django.db.models import Q
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now, timedelta

from carservice.models import Car, Offer, Rent
from carservice.views import RentCreateView


class TestCarCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_car_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('car_create'), {
            'vin': '1G8MG35X48Y106575',
            'car_mileage': 123456,
            'car_brand': 'Opel',
            'car_model': 'Astra',
            'date_of_prod': '2023'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.first().user, self.user)


class TestCarReadView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='testsuperuser', password='testpassword')
        self.car = Car.objects.create(
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod='2023',
            user=self.user
        )

    def test_get_queryset_superuser(self):
        self.client.login(username='testsuperuser', password='testpassword')
        response = self.client.get(reverse('car_read'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 1)
        self.assertEqual(response.context['cars'][0], self.car)

    def test_get_queryset_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('car_read'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 1)
        self.assertEqual(response.context['cars'][0], self.car)


class TestCarUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )

    def test_car_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('update_car', kwargs={'car_id': self.car.id}), {
            'vin': 'JH4DB1550LS000111',
            'car_mileage': 987654,
            'car_brand': 'Opel',
            'car_model': 'Astra II',
            'date_of_prod': 2023
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('car_read'))
        self.assertEqual(Car.objects.count(), 1)
        updated_car = Car.objects.first()
        self.assertEqual(updated_car.vin, 'JH4DB1550LS000111')
        self.assertEqual(updated_car.car_mileage, 987654)
        self.assertEqual(updated_car.car_brand, 'Opel')
        self.assertEqual(updated_car.car_model, 'Astra II')
        self.assertEqual(updated_car.date_of_prod, 2023)

    def test_car_update_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('update_car', kwargs={'car_id': self.car.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_update.html')

    def test_car_update_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('update_car', kwargs={'car_id': self.car.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_update.html')


class TestCarDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )

    def test_car_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(reverse('delete_car', kwargs={'pk': self.car.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('car_read'))
        self.assertEqual(Car.objects.count(), 0)


class TestOfferSearchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )

    def test_carsearch_with_brand_and_model_terms(self):
        url = reverse('carsearch')
        search_term = 'Opel Astra'
        self.client.force_login(self.user)
        response = self.client.get(url, {'search': search_term})
        offers = response.context['offers']
        expected_offers = Offer.objects.filter(car__car_brand__iexact='Opel', car__car_model__iexact='Astra')
        self.assertQuerySetEqual(offers, expected_offers, transform=lambda x: x)

    def test_carsearch_with_brand_term(self):
        url = reverse('carsearch')
        search_term = 'Opel'
        self.client.force_login(self.user)
        response = self.client.get(url, {'search': search_term})
        offers = response.context['offers']
        expected_offers = Offer.objects.filter(Q(car__car_brand__iexact='Opel') | Q(car__car_model__iexact='Opel'))
        self.assertQuerySetEqual(offers, expected_offers, transform=lambda x: x)

    def test_carsearch_with_model_term(self):
        url = reverse('carsearch')
        search_term = 'Astra'
        self.client.force_login(self.user)
        response = self.client.get(url, {'search': search_term})
        offers = response.context['offers']
        expected_offers = Offer.objects.filter(car__car_model__iexact='Astra')
        self.assertQuerySetEqual(offers, expected_offers, transform=lambda x: x)


class OfferResultViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )

    def test_offer_result_view(self):
        self.client.force_login(self.user)
        url = reverse('offer_result', args=[self.car.id, self.offer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer_result.html')
        self.assertEqual(response.context['car'], self.car)
        self.assertEqual(response.context['offer'], self.offer)

    def test_offer_result_view_with_invalid_car_id(self):
        self.client.force_login(self.user)
        invalid_car_id = 9999
        url = reverse('offer_result', args=[invalid_car_id, self.offer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_offer_result_view_with_invalid_offer_id(self):
        self.client.force_login(self.user)
        invalid_offer_id = 9999
        url = reverse('offer_result', args=[self.car.id, invalid_offer_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestOfferCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )


class TestOfferUpdateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )

    def test_offer_update_view_get(self):
        self.client.force_login(self.user)
        url = reverse('offer_update', args=[self.offer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer_update.html')
        self.assertEqual(response.context['offer'], self.offer)

    def test_offer_update_view_post(self):
        self.client.force_login(self.user)
        url = reverse('offer_update', args=[self.offer.id])
        data = {
            'price': 456,
            'description': 'updated description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_offer = Offer.objects.get(id=self.offer.id)
        self.assertEqual(updated_offer.price, 456)
        self.assertEqual(updated_offer.description, 'updated description')
        self.assertRedirects(response, reverse('offer_read'))


class TestOfferDeleteView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )

    def test_offer_delete_view_get(self):
        self.client.force_login(self.user)
        url = reverse('offer_delete', args=[self.offer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer_delete.html')
        self.assertEqual(response.context['offer'], self.offer)

    def test_offer_delete_view_post(self):
        self.client.force_login(self.user)
        url = reverse('offer_delete', args=[self.offer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Offer.DoesNotExist):
            Offer.objects.get(id=self.offer.id)
        self.assertRedirects(response, reverse('offer_read'))


class TestRentCreateView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            car_photo='test_photo',
            vin='1G8MG35X48Y106575',
            car_mileage=123456,
            car_brand='Opel',
            car_model='Astra',
            date_of_prod=2022,
            user=self.user
        )
        self.offer = Offer.objects.create(
            car=self.car,
            price=123,
            description='test description',
            user=self.user
        )
        self.rent = Rent.objects.create(
            rent_start=datetime.date.today(),
            duration=1,
            offer=self.offer,
            user=self.user
        )

    def test_get_initial(self):
        view = RentCreateView()
        initial = view.get_initial()
        rent_start = initial['rent_start']
        current_time = now()
        max_difference = timedelta(milliseconds=5)
        self.assertAlmostEqual(rent_start, current_time, delta=max_difference)
