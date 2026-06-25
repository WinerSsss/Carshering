from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CarViewSet, OfferViewSet, RentViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'rents', RentViewSet, basename='rent')

urlpatterns = [
    path('', include(router.urls)),
]

# Made with Bob
