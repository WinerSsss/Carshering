import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from carservice.models import Car, Offer, Rent
from datetime import date, timedelta


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='testpass123'
    )


@pytest.fixture
def car(db, user):
    return Car.objects.create(
        vin='1HGBH41JXMN109186',
        car_mileage=50000,
        car_brand='Toyota',
        car_model='Camry',
        date_of_prod=2020,
        user=user
    )


@pytest.fixture
def offer(db, car, user):
    return Offer.objects.create(
        description='Great car for rent',
        price=50.0,
        car=car,
        user=user
    )


@pytest.mark.django_db
class TestCarAPI:
    """Test Car API endpoints"""
    
    def test_list_cars_unauthenticated(self, api_client, car):
        """Unauthenticated users can list cars"""
        url = reverse('car-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_car_authenticated(self, api_client, user):
        """Authenticated users can create cars"""
        api_client.force_authenticate(user=user)
        url = reverse('car-list')
        data = {
            'vin': '1HGBH41JXMN109187',
            'car_mileage': 30000,
            'car_brand': 'Honda',
            'car_model': 'Civic',
            'date_of_prod': 2021
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Car.objects.count() == 1
    
    def test_create_car_unauthenticated(self, api_client):
        """Unauthenticated users cannot create cars"""
        url = reverse('car-list')
        data = {
            'vin': '1HGBH41JXMN109187',
            'car_mileage': 30000,
            'car_brand': 'Honda',
            'car_model': 'Civic',
            'date_of_prod': 2021
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_own_car(self, api_client, user, car):
        """Users can update their own cars"""
        api_client.force_authenticate(user=user)
        url = reverse('car-detail', kwargs={'pk': car.pk})
        data = {'car_mileage': 60000}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        car.refresh_from_db()
        assert car.car_mileage == 60000
    
    def test_cannot_update_other_user_car(self, api_client, other_user, car):
        """Users cannot update other users' cars"""
        api_client.force_authenticate(user=other_user)
        url = reverse('car-detail', kwargs={'pk': car.pk})
        data = {'car_mileage': 60000}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_filter_cars_by_brand(self, api_client, car):
        """Test filtering cars by brand"""
        url = reverse('car-list')
        response = api_client.get(url, {'car_brand': 'Toyota'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_search_cars(self, api_client, car):
        """Test searching cars"""
        url = reverse('car-list')
        response = api_client.get(url, {'search': 'Camry'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_my_cars_endpoint(self, api_client, user, car):
        """Test my_cars custom action"""
        api_client.force_authenticate(user=user)
        url = reverse('car-my-cars')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestOfferAPI:
    """Test Offer API endpoints"""
    
    def test_list_offers(self, api_client, offer):
        """Test listing offers"""
        url = reverse('offer-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_offer_authenticated(self, api_client, user, car):
        """Authenticated users can create offers for their cars"""
        api_client.force_authenticate(user=user)
        url = reverse('offer-list')
        data = {
            'description': 'New offer',
            'price': 45.0,
            'car_id': car.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Offer.objects.count() == 1
    
    def test_cannot_create_offer_for_other_user_car(self, api_client, other_user, car):
        """Users cannot create offers for other users' cars"""
        api_client.force_authenticate(user=other_user)
        url = reverse('offer-list')
        data = {
            'description': 'New offer',
            'price': 45.0,
            'car_id': car.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_filter_offers_by_price(self, api_client, offer):
        """Test filtering offers by price range"""
        url = reverse('offer-list')
        response = api_client.get(url, {'min_price': 40, 'max_price': 60})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_filter_available_offers(self, api_client, offer):
        """Test filtering available offers"""
        url = reverse('offer-list')
        response = api_client.get(url, {'available': 'true'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_available_offers_endpoint(self, api_client, offer):
        """Test available offers custom action"""
        url = reverse('offer-available')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1


@pytest.mark.django_db
class TestRentAPI:
    """Test Rent API endpoints"""
    
    def test_create_rent_authenticated(self, api_client, user, offer):
        """Authenticated users can create rents"""
        api_client.force_authenticate(user=user)
        url = reverse('rent-list')
        data = {
            'offer_id': offer.id,
            'rent_start': date.today() + timedelta(days=1),
            'duration': 5
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Rent.objects.count() == 1
    
    def test_create_rent_unauthenticated(self, api_client, offer):
        """Unauthenticated users cannot create rents"""
        url = reverse('rent-list')
        data = {
            'offer_id': offer.id,
            'rent_start': date.today() + timedelta(days=1),
            'duration': 5
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_list_own_rents_only(self, api_client, user, other_user, offer):
        """Users can only see their own rents"""
        # Create rent for user
        api_client.force_authenticate(user=user)
        Rent.objects.create(
            offer=offer,
            user=user,
            rent_start=date.today() + timedelta(days=1),
            duration=5
        )
        
        # Other user should not see it
        api_client.force_authenticate(user=other_user)
        url = reverse('rent-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0
    
    def test_close_rent(self, api_client, user, offer):
        """Test closing a rent"""
        api_client.force_authenticate(user=user)
        rent = Rent.objects.create(
            offer=offer,
            user=user,
            rent_start=date.today(),
            duration=5
        )
        
        url = reverse('rent-close', kwargs={'pk': rent.pk})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        rent.refresh_from_db()
        assert rent.close_rent is True
    
    def test_active_rents_endpoint(self, api_client, user, offer):
        """Test active rents custom action"""
        api_client.force_authenticate(user=user)
        Rent.objects.create(
            offer=offer,
            user=user,
            rent_start=date.today(),
            duration=5
        )
        
        url = reverse('rent-active')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_rent_history_endpoint(self, api_client, user, offer):
        """Test rent history custom action"""
        api_client.force_authenticate(user=user)
        rent = Rent.objects.create(
            offer=offer,
            user=user,
            rent_start=date.today(),
            duration=5
        )
        rent.close_rent = True
        rent.save()
        
        url = reverse('rent-history')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_cannot_rent_already_rented_car(self, api_client, user, other_user, offer):
        """Cannot create rent for already rented car"""
        # First user creates a rent
        api_client.force_authenticate(user=user)
        Rent.objects.create(
            offer=offer,
            user=user,
            rent_start=date.today(),
            duration=5
        )
        
        # Second user tries to rent the same car
        api_client.force_authenticate(user=other_user)
        url = reverse('rent-list')
        data = {
            'offer_id': offer.id,
            'rent_start': date.today() + timedelta(days=1),
            'duration': 3
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAPIPagination:
    """Test API pagination"""
    
    def test_car_pagination(self, api_client, user):
        """Test that car list is paginated"""
        # Create 15 cars
        for i in range(15):
            Car.objects.create(
                vin=f'1HGBH41JXMN10918{i}',
                car_mileage=50000 + i * 1000,
                car_brand='Toyota',
                car_model=f'Model{i}',
                date_of_prod=2020,
                user=user
            )
        
        url = reverse('car-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert response.data['count'] == 15
        assert len(response.data['results']) == 10  # Default page size


@pytest.mark.django_db
class TestAPIOrdering:
    """Test API ordering"""
    
    def test_car_ordering_by_year(self, api_client, user):
        """Test ordering cars by production year"""
        Car.objects.create(
            vin='1HGBH41JXMN109186',
            car_mileage=50000,
            car_brand='Toyota',
            car_model='Old',
            date_of_prod=2018,
            user=user
        )
        Car.objects.create(
            vin='1HGBH41JXMN109187',
            car_mileage=30000,
            car_brand='Toyota',
            car_model='New',
            date_of_prod=2022,
            user=user
        )
        
        url = reverse('car-list')
        response = api_client.get(url, {'ordering': '-date_of_prod'})
        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        assert results[0]['car_model'] == 'New'
        assert results[1]['car_model'] == 'Old'

# Made with Bob
