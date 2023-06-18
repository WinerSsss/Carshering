from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Car(models.Model):
    serial_number = models.CharField(max_length=17)
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


class Rent(models.Model):
    status = models.BooleanField(default=True)
    rent_start = models.DateField(null=True)
    rent_stop = models.DateField(null=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: {self.rent_duration}, offer: {self.id_offer}, user: {self.id_user}'