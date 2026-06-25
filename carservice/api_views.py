from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters import rest_framework as filters_rf
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Car, Offer, Rent
from .serializers import (
    CarSerializer, CarListSerializer,
    OfferSerializer, OfferListSerializer,
    RentSerializer, RentListSerializer, RentUpdateSerializer
)


class CarFilter(filters_rf.FilterSet):
    """Filter for Car model"""
    car_brand = filters_rf.CharFilter(lookup_expr='iexact')
    car_model = filters_rf.CharFilter(lookup_expr='icontains')
    min_year = filters_rf.NumberFilter(field_name='date_of_prod', lookup_expr='gte')
    max_year = filters_rf.NumberFilter(field_name='date_of_prod', lookup_expr='lte')
    max_mileage = filters_rf.NumberFilter(field_name='car_mileage', lookup_expr='lte')
    
    class Meta:
        model = Car
        fields = ['car_brand', 'car_model', 'min_year', 'max_year', 'max_mileage']


@extend_schema_view(
    list=extend_schema(
        description="List all cars with filtering and sorting options",
        parameters=[
            OpenApiParameter(name='car_brand', description='Filter by car brand', type=str),
            OpenApiParameter(name='car_model', description='Filter by car model (partial match)', type=str),
            OpenApiParameter(name='min_year', description='Minimum production year', type=int),
            OpenApiParameter(name='max_year', description='Maximum production year', type=int),
            OpenApiParameter(name='max_mileage', description='Maximum mileage', type=int),
            OpenApiParameter(name='ordering', description='Order by field (e.g., -date_of_prod)', type=str),
        ]
    ),
    retrieve=extend_schema(description="Get detailed information about a specific car"),
    create=extend_schema(description="Create a new car (authenticated users only)"),
    update=extend_schema(description="Update car details (owner only)"),
    partial_update=extend_schema(description="Partially update car details (owner only)"),
    destroy=extend_schema(description="Delete a car (owner only)"),
)
class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing cars.
    
    Provides CRUD operations for cars with filtering, searching, and ordering.
    """
    queryset = Car.objects.select_related('user').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['car_brand', 'car_model', 'vin']
    ordering_fields = ['date_of_prod', 'car_mileage', 'car_brand']
    ordering = ['-date_of_prod']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        return CarSerializer
    
    def get_queryset(self):
        """Filter cars based on user permissions"""
        queryset = super().get_queryset()
        
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only show user's own cars for modification
            return queryset.filter(user=self.request.user)
        
        # Show all cars for listing and detail views
        return queryset
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_cars(self, request):
        """Get cars owned by the current user"""
        cars = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)


class OfferFilter(filters_rf.FilterSet):
    """Filter for Offer model"""
    min_price = filters_rf.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters_rf.NumberFilter(field_name='price', lookup_expr='lte')
    car_brand = filters_rf.CharFilter(field_name='car__car_brand', lookup_expr='iexact')
    car_model = filters_rf.CharFilter(field_name='car__car_model', lookup_expr='icontains')
    available = filters_rf.BooleanFilter(method='filter_available')
    
    class Meta:
        model = Offer
        fields = ['min_price', 'max_price', 'car_brand', 'car_model', 'available']
    
    def filter_available(self, queryset, name, value):
        """Filter offers that don't have active rents"""
        if value:
            # Get offers with no active rents
            active_rent_offers = Rent.objects.filter(
                close_rent=False,
                status__in=[Rent.PENDING, Rent.ACTIVE]
            ).values_list('offer_id', flat=True)
            
            return queryset.exclude(id__in=active_rent_offers)
        return queryset


@extend_schema_view(
    list=extend_schema(
        description="List all offers with filtering and sorting options",
        parameters=[
            OpenApiParameter(name='min_price', description='Minimum price', type=float),
            OpenApiParameter(name='max_price', description='Maximum price', type=float),
            OpenApiParameter(name='car_brand', description='Filter by car brand', type=str),
            OpenApiParameter(name='car_model', description='Filter by car model', type=str),
            OpenApiParameter(name='available', description='Show only available offers', type=bool),
            OpenApiParameter(name='ordering', description='Order by field (e.g., price, -price)', type=str),
        ]
    ),
    retrieve=extend_schema(description="Get detailed information about a specific offer"),
    create=extend_schema(description="Create a new offer (authenticated users only)"),
    update=extend_schema(description="Update offer details (owner only)"),
    partial_update=extend_schema(description="Partially update offer details (owner only)"),
    destroy=extend_schema(description="Delete an offer (owner only)"),
)
class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing offers.
    
    Provides CRUD operations for offers with filtering, searching, and ordering.
    """
    queryset = Offer.objects.select_related('car', 'user').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['description', 'car__car_brand', 'car__car_model']
    ordering_fields = ['price', 'id']
    ordering = ['price']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        return OfferSerializer
    
    def get_queryset(self):
        """Filter offers based on user permissions"""
        queryset = super().get_queryset()
        
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only show user's own offers for modification
            return queryset.filter(user=self.request.user)
        
        return queryset
    
    @method_decorator(cache_page(60 * 2))  # Cache for 2 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_offers(self, request):
        """Get offers created by the current user"""
        offers = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available offers (no active rents)"""
        active_rent_offers = Rent.objects.filter(
            close_rent=False,
            status__in=[Rent.PENDING, Rent.ACTIVE]
        ).values_list('offer_id', flat=True)
        
        offers = self.queryset.exclude(id__in=active_rent_offers)
        
        page = self.paginate_queryset(offers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)


class RentFilter(filters_rf.FilterSet):
    """Filter for Rent model"""
    status = filters_rf.ChoiceFilter(choices=Rent.STATUS_CHOICES)
    start_date = filters_rf.DateFilter(field_name='rent_start', lookup_expr='gte')
    end_date = filters_rf.DateFilter(field_name='rent_end', lookup_expr='lte')
    active = filters_rf.BooleanFilter(field_name='close_rent', lookup_expr='exact', 
                                      exclude=True)
    
    class Meta:
        model = Rent
        fields = ['status', 'start_date', 'end_date', 'active']


@extend_schema_view(
    list=extend_schema(
        description="List all rents with filtering and sorting options",
        parameters=[
            OpenApiParameter(name='status', description='Filter by rent status', type=str),
            OpenApiParameter(name='start_date', description='Filter by start date (YYYY-MM-DD)', type=OpenApiTypes.DATE),
            OpenApiParameter(name='end_date', description='Filter by end date (YYYY-MM-DD)', type=OpenApiTypes.DATE),
            OpenApiParameter(name='active', description='Show only active rents', type=bool),
            OpenApiParameter(name='ordering', description='Order by field (e.g., -rent_start)', type=str),
        ]
    ),
    retrieve=extend_schema(description="Get detailed information about a specific rent"),
    create=extend_schema(description="Create a new rent (authenticated users only)"),
    update=extend_schema(description="Update rent details (renter only)"),
    partial_update=extend_schema(description="Partially update rent details (renter only)"),
    destroy=extend_schema(description="Delete a rent (renter only)"),
)
class RentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing rents.
    
    Provides CRUD operations for rents with filtering, searching, and ordering.
    """
    queryset = Rent.objects.select_related('offer__car', 'user').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RentFilter
    ordering_fields = ['rent_start', 'rent_end', 'status']
    ordering = ['-rent_start']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RentListSerializer
        elif self.action == 'close':
            return RentUpdateSerializer
        return RentSerializer
    
    def get_queryset(self):
        """Filter rents to show only user's rents"""
        return super().get_queryset().filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a rent"""
        rent = self.get_object()
        
        if rent.close_rent:
            return Response(
                {'detail': 'Rent is already closed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RentUpdateSerializer(rent, data={'close_rent': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(RentSerializer(rent).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active rents for the current user"""
        rents = self.get_queryset().filter(
            close_rent=False,
            status__in=[Rent.PENDING, Rent.ACTIVE]
        )
        
        page = self.paginate_queryset(rents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(rents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get rent history (closed rents) for the current user"""
        rents = self.get_queryset().filter(close_rent=True)
        
        page = self.paginate_queryset(rents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(rents, many=True)
        return Response(serializer.data)

# Made with Bob
