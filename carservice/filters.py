from .models import Car
import django_filters

class CarFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = ['car_brand', 'car_model']
