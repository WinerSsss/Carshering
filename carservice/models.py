from django.db import models
from django.core.validators import MaxValueValidator


class Car(models.Model):
    serial_number = models.IntegerField(validators=[MaxValueValidator(100)])
    car_mileage = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    car_model = models.CharField(max_length=30)
    car_year = models.DateField()

    def __str__(self):
        return f'Model: {self.car_model}, serial number:({self.serial_number})'


class Offer(models.Model):
    description = models.TextField()
    price = models.FloatField(validators=[MaxValueValidator(10.0)])

    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'Price: ({self.price}), car:({self.id_car})'


class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f'Name: {self.name} {self.surname}'


class Rent(models.Model):
    status = models.BooleanField(default=True)
    rent_duration = models.DurationField()

    id_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: {self.rent_duration}, offer: {self.id_offer}, user: {self.id_user}'