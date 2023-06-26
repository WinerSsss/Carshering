from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date, timedelta
from Carshering.settings import RENT_LENGTH_IN_DAYS


def vin_validator(vin_number):
    '''
    Validate the VIN (Vehicle Identification Number) using the following formula:
    - Transliterate letters to their numerical counterparts.
    - Multiply the numbers by their assigned weights.
    - Add up the products.
    - Divide the total sum by 11 to find the remainder.
    - If the remainder is 10, the check digit should be "X".
    - Compare the calculated remainder with the expected check digit.

    Parameters:
        vin_number (str): The VIN to be validated.

    Returns:
        bool: True if the VIN is valid, False otherwise.
    '''
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


def check_vin_number(vin_number):
    if len(vin_number) != 17:
        raise ValidationError(
            _('VIN number is too short.'),
            params={'vin_number': vin_number},
        )
    if not vin_number.isalnum():
        raise ValidationError(
            _('VIN number should contain only letters and numbers.'),
            params={'vin_number': vin_number},
        )
    if not vin_validator(vin_number):
        raise ValidationError(
            _('Enter the valid VIN number.'),
            params={'vin_number': vin_number},
        )


def validate_year(prod_year):
    first_made_car = date(1886, 1, 29)
    if prod_year < first_made_car:
        raise ValidationError(
            _('You can\'t enter the year before the first car was made.'),
            params={'prod_year': prod_year},
        )
    if prod_year > date.today():
        raise ValidationError(
            _('You can\'t add the car from future.'),
            params={'prod_year': prod_year},
        )


def check_car_exists(car_number):
    if Car.objects.filter(serial_number=car_number).exists():
        raise ValidationError(
            _('Car with this VIN number already exists.'),
            params={'car_number': car_number},
        )


def validate_mileage(mileage):
    if mileage > 1000000:
        raise ValidationError(
            _('You can\'t add the car with more than 1 000 000 km.'),
            params={'mileage': mileage},
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
    serial_number = models.CharField(max_length=17, validators=[check_vin_number, check_car_exists])
    car_mileage = models.PositiveIntegerField(validators=[validate_mileage])
    car_brand = models.CharField(max_length=30, choices=BRAND_CHOICES)
    car_model = models.CharField(max_length=30)
    date_of_prod = models.DateField(null=True, validators=[validate_year])

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'Model: {self.car_model, self.car_brand}, serial number:({self.serial_number})'


def car_available(vin_number):
    if Offer.objects.filter(car=vin_number).exists():
        raise ValidationError(
            _('This car is already offered.'),
            params={'vin_number': vin_number},
        )


class Offer(models.Model):
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(10.0)])

    car = models.OneToOneField(Car, on_delete=models.CASCADE, validators=[car_available])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Price: ({self.price}), car:({self.car})'


def past_rent(rent_date):
    if rent_date < date.today():
        raise ValidationError(
            _('Enter a valid date.'),
            params={'rent_date': rent_date},
        )


def rent_length(rent_date):
    if rent_date > date.today() + RENT_LENGTH_IN_DAYS:
        raise ValidationError(
            _('You can rent a car for a month maximum.'),
            params={'rent_date': rent_date},
        )


def future_rent(rent_date):
    two_weeks = timedelta(days=14)
    if rent_date > date.today() + two_weeks:
        raise ValidationError(
            _('You can rent a car for a maximum of two weeks in advance.'),
            params={'rent_date': rent_date},
        )


def offer_available(vin_number):
    if Rent.objects.filter(offer=vin_number).exists():
        raise ValidationError(
            _('This offer is already rented.'),
            params={'vin_number': vin_number},
        )


class Rent(models.Model):
    ACTIVE = 'active'
    FINISHED = 'finished'
    OVERDUE = 'overdue'

    STATUS_CHOICES = [
        (ACTIVE, 'Rent active'),
        (FINISHED, 'Rent finished'),
        (OVERDUE, 'Rent overdue'),
    ]

    status = models.CharField(max_length=30, blank=True, null=True, choices=STATUS_CHOICES, default=ACTIVE)
    rent_start = models.DateField(null=True, validators=[past_rent, future_rent, rent_length])
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(30)])

    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, validators=[offer_available])
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rent status: {self.status}, rent duration: ({self.duration}), offer: {self.offer}, user: {self.user}'
