from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from Carshering.settings import RENT_LENGTH_IN_DAYS
from django.utils.timezone import now


def vin_validator(vin):
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

    if len(vin) != 17:
        return False

    checksum = 0

    for index, char in enumerate(vin):
        if index == 8:
            continue
        if char.isdigit():
            value = int(char)
        else:
            value = values.get(char.upper())
            if value is None:
                return False

        checksum += value * weights[index + 1]

    if vin[8].isdigit():
        expected_checksum = int(vin[8])
    else:
        expected_checksum = 10

    return checksum % 11 == expected_checksum


def check_vin_number(vin):
    if len(vin) != 17:
        raise ValidationError(
            _('VIN is too short.'),
            params={'vin': vin},
        )
    if not vin.isalnum():
        raise ValidationError(
            _('VIN should contain only letters and numbers.'),
            params={'vin_number': vin},
        )
    if not vin_validator(vin):
        raise ValidationError(
            _('Enter the valid VIN.'),
            params={'vin': vin},
        )


def validate_year(prod_year):
    if prod_year < 1886:
        raise ValidationError(
            _('You can\'t enter the year before the first car was made.'),
            params={'prod_year': prod_year},
        )
    if prod_year > date.today().year:
        raise ValidationError(
            _('You can\'t add the car from future.'),
            params={'prod_year': prod_year},
        )
    if len(str(prod_year)) != 4:
        raise ValidationError(
            _('Enter the valid year.'),
            params={'prod_year': prod_year},
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
    car_photo = models.ImageField(upload_to='static/image', null=True)
    vin = models.CharField(max_length=17, validators=[check_vin_number], unique=True)
    car_mileage = models.PositiveIntegerField(validators=[validate_mileage])
    car_brand = models.CharField(max_length=15, choices=BRAND_CHOICES)
    car_model = models.CharField(max_length=15)
    date_of_prod = models.IntegerField(null=True, validators=[validate_year])

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Model: {self.car_model, self.car_brand}, vin number:({self.vin})'


class Offer(models.Model):
    description = models.TextField(max_length=300)
    price = models.FloatField(validators=[MinValueValidator(10.0)])

    car = models.OneToOneField(Car, on_delete=models.CASCADE)
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
    if rent_date > date.today() + timedelta(RENT_LENGTH_IN_DAYS):
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


    status = models.CharField(max_length=30, blank=True, null=True, choices=STATUS_CHOICES)
    rent_start = models.DateField(null=True, validators=[past_rent, future_rent, rent_length])
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(30)])
    rent_end = models.DateField(null=True, validators=[past_rent])

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    close_rent = models.BooleanField(default=False)


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
