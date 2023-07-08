from datetime import timedelta

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now

from .validators import (
    check_vin_number, validate_mileage, validate_year, past_rent, future_rent
    )


class Car(models.Model):
    BRAND_CHOICES = (
        ('Volkswagen', 'Volkswagen'),
        ('BMW', 'BMW'),
        ('Audi', 'Audi'),
        ('Ford', 'Ford'),
        ('Opel', 'Opel'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Renault', 'Renault'),
        ('Skoda', 'Skoda'),
        ('Toyota', 'Toyota'),
        ('Peugeot', 'Peugeot'),
        ('Hyundai', 'Hyundai'),
        ('Citroën', 'Citroën'),
        ('Volvo', 'Volvo'),
        ('Nissan', 'Nissan'),
        ('Fiat', 'Fiat'),
        ('Seat', 'Seat'),
        ('Mazda', 'Mazda'),
        ('Honda', 'Honda'),
        ('Suzuki', 'Suzuki'),
        ('Jeep', 'Jeep'),
        ('Dacia', 'Dacia'),
        ('Mitsubishi', 'Mitsubishi'),
        ('MINI', 'MINI'),
        ('Other', 'Other'),
    )

    car_photo = models.ImageField(upload_to='static/image', null=True)
    vin = models.CharField(max_length=17, validators=[check_vin_number], unique=True)
    car_mileage = models.PositiveIntegerField(validators=[validate_mileage])
    car_brand = models.CharField(max_length=15, choices=BRAND_CHOICES)
    car_model = models.CharField(max_length=15)
    date_of_prod = models.IntegerField(null=True, validators=[validate_year])

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Model: {self.car_model} {self.car_brand}, vin number: ({self.vin})'


class Offer(models.Model):
    description = models.TextField(max_length=300)
    price = models.FloatField(validators=[MinValueValidator(10.0)])

    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Price: ({self.price}), car:({self.car.car_model} {self.car.car_brand})'


class Rent(models.Model):
    PENDING = 'pending'
    ACTIVE = 'Rent active'
    FINISHED = 'Rent finished'
    OVERDUE = 'Rent overdue'

    STATUS_CHOICES = [
        (PENDING, 'pending'),
        (ACTIVE, 'Rent active'),
        (FINISHED, 'Rent finished'),
        (OVERDUE, 'Rent overdue'),
    ]

    status = models.CharField(
        max_length=30, blank=True, null=True, choices=STATUS_CHOICES
    )
    rent_start = models.DateField(null=True, validators=[past_rent, future_rent])
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(30), MinValueValidator(1)])
    rent_end = models.DateField(null=True, validators=[past_rent])
    close_rent = models.BooleanField(default=False)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.rent_end = self.rent_start + timedelta(days=self.duration)
        if self.rent_start > now().date():
            self.status = self.PENDING
        else:
            self.status = self.ACTIVE
        if self.close_rent:
            self.status = self.FINISHED
            self.rent_end = now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: ({self.duration}), offer: {self.offer}, user: {self.user}'
