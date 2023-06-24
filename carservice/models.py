from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date, timedelta


def vin_validator(vin_number):
    values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
        'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
    }

    weights = {
        1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 10, 9: 0, 10: 9,
        11: 8, 12: 7, 13: 6, 14: 5, 15: 4, 16: 3, 17: 2
    }

    if len(vin_number) != 17:
        return False

    checksum = 0

    for index, char in enumerate(vin_number):
        if index == 8:
            continue
        if char.isdigit():
            value = int(char)
        else:
            value = values.get(char.upper())
            if value is None:
                return False

        checksum += value * weights[index + 1]

    if vin_number[8].isdigit():
        expected_checksum = int(vin_number[8])
    else:
        expected_checksum = 10

    return checksum % 11 == expected_checksum


def validate_ser_num(value):
    if len(value) != 17:
        raise ValidationError(
            _('VIN number is too short.'),
            params={"value": value},
        )
    if not value.isalnum():
        raise ValidationError(
            _('VIN number should contain only letters and numbers.'),
            params={"value": value},
        )
    if not vin_validator(value):
        raise ValidationError(
            _('Enter the valid VIN number.'),
            params={"value": value},
        )


def validate_year(value):
    first_made_car = datetime.strptime('1886-01-29', '%Y-%m-%d').date()
    if value < first_made_car:
        raise ValidationError(
            _('You can\'t enter the year before the first car was made.'),
            params={"value": value},
        )
    if value > date.today():
        raise ValidationError(
            _('You can\'t add the car from future.'),
            params={"value": value},
        )


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


class Car(models.Model):
    serial_number = models.CharField(max_length=17, validators=[validate_ser_num])
    car_mileage = models.PositiveIntegerField()
    car_brand = models.CharField(max_length=30, choices=BRAND_CHOICES)
    car_model = models.CharField(max_length=30)
    year_of_prod = models.DateField(null=True, validators=[validate_year])

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'Model: {self.car_model, self.car_brand}, serial number:({self.serial_number})'


class Offer(models.Model):
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(10.0)])

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Price: ({self.price}), car:({self.car})'


ACTIVE = 'active'
FINISHED = 'finished'

STATUS_CHOICES = [
    (ACTIVE, 'Rent active'),
    (FINISHED, 'Rent finished'),
]


def val_rent(value):
    if value < date.today():
        raise ValidationError(
            _('Enter a valid date.'),
            params={"value": value},
        )


def rent_length(value):
    month = timedelta(days=30)
    if value > date.today() + month:
        raise ValidationError(
            _('You can rent a car for a month maximum.'),
            params={"value": value},
        )


def future_rent(value):
    two_weeks = timedelta(days=14)
    if value > date.today() + two_weeks:
        raise ValidationError(
            _('You can rent a car for a maximum of two weeks in advance.'),
            params={"value": value},
        )


class Rent(models.Model):
    status = models.CharField(max_length=30, blank=True, null=True, choices=STATUS_CHOICES, default=ACTIVE)
    rent_start = models.DateField(null=True, validators=[val_rent, future_rent])
    rent_stop = models.DateField(null=True, validators=[val_rent, rent_length])

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: ({self.rent_start} - {self.rent_stop}), offer: {self.offer}, user: {self.user}'
