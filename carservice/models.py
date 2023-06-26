from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_ser_num(value):
    if len(value) != 17:
        raise ValidationError(
            _('Please, put the correct VIN number.'),
            params={"value": value},
        )


class Car(models.Model):
    serial_number = models.CharField(max_length=17, validators=[validate_ser_num])
    car_mileage = models.PositiveIntegerField()
    car_model = models.CharField(max_length=30)
    car_year = models.DateField()

    def __str__(self):
        return f'Model: {self.car_model}, serial number:({self.serial_number})'


class Offer(models.Model):
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(10.0)])

    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'Price: ({self.price}), car:({self.car})'


STATUS_CHOICES = [
    ('active', 'Rent active'),
    ('finished', 'Rent finished'),
]


class Rent(models.Model):
    status = models.CharField(max_length=30, blank=True, null=True, choices=STATUS_CHOICES)
    rent_start = models.DateField(null=True)
    rent_stop = models.DateField(null=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: ({self.rent_start} - {self.rent_stop}), offer: {self.offer}, user: {self.user}'
