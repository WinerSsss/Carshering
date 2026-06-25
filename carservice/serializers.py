from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Car, Offer, Rent


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Car
        fields = [
            'id', 'car_photo', 'vin', 'car_mileage', 'car_brand', 
            'car_model', 'date_of_prod', 'user', 'user_id'
        ]
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CarListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for car listings"""
    
    class Meta:
        model = Car
        fields = ['id', 'car_brand', 'car_model', 'date_of_prod', 'car_photo']


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model"""
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Offer
        fields = [
            'id', 'description', 'price', 'car', 'car_id', 
            'user', 'user_id'
        ]
        read_only_fields = ['id', 'user', 'car']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_car_id(self, value):
        """Ensure the car belongs to the user"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                car = Car.objects.get(id=value, user=request.user)
            except Car.DoesNotExist:
                raise serializers.ValidationError(
                    "Car not found or you don't have permission to create an offer for this car."
                )
        return value


class OfferListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for offer listings"""
    car_brand = serializers.CharField(source='car.car_brand', read_only=True)
    car_model = serializers.CharField(source='car.car_model', read_only=True)
    car_photo = serializers.ImageField(source='car.car_photo', read_only=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'price', 'car_brand', 'car_model', 'car_photo']


class RentSerializer(serializers.ModelSerializer):
    """Serializer for Rent model"""
    offer = OfferSerializer(read_only=True)
    offer_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Rent
        fields = [
            'id', 'status', 'rent_start', 'duration', 'rent_end', 
            'close_rent', 'offer', 'offer_id', 'user', 'user_id'
        ]
        read_only_fields = ['id', 'status', 'rent_end', 'user', 'offer']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_offer_id(self, value):
        """Ensure the offer exists and is available"""
        try:
            offer = Offer.objects.get(id=value)
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Offer not found.")
        
        # Check if there are any active rents for this offer
        active_rents = Rent.objects.filter(
            offer=offer,
            close_rent=False,
            status__in=[Rent.PENDING, Rent.ACTIVE]
        )
        
        if active_rents.exists():
            raise serializers.ValidationError(
                "This car is already rented or has a pending rental."
            )
        
        return value


class RentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for rent listings"""
    car_brand = serializers.CharField(source='offer.car.car_brand', read_only=True)
    car_model = serializers.CharField(source='offer.car.car_model', read_only=True)
    price = serializers.FloatField(source='offer.price', read_only=True)
    
    class Meta:
        model = Rent
        fields = [
            'id', 'status', 'rent_start', 'rent_end', 'duration',
            'car_brand', 'car_model', 'price'
        ]


class RentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating rent status"""
    
    class Meta:
        model = Rent
        fields = ['close_rent']
    
    def validate_close_rent(self, value):
        """Only allow closing rents, not reopening them"""
        if not value and self.instance and self.instance.close_rent:
            raise serializers.ValidationError(
                "Cannot reopen a closed rent."
            )
        return value

# Made with Bob
