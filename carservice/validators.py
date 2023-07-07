from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def vin_validator(vin):
    """
    Validate the VIN (Vehicle Identification Number) using the following formula:
    - Transliterate letters to their numerical counterparts.
    - Multiply the numbers by their assigned weights.
    - Add up the products.
    - Divide the total sum by 11 to find the remainder.
    - If the remainder is 10, the check digit should be "X".
    - Compare the calculated remainder with the expected check digit.

    Parameters:
        vin: (str): The VIN to be validated.

    Returns:
        bool: True if the VIN is valid, False otherwise.
    """
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
    """
    Check if the VIN is not too short, contains only letters and numbers and is valid. Call vin_validator function.

    Parameters:
        vin:

    Returns:
        None
    """
    if not vin_validator(vin):
        raise ValidationError(
            _('VIN is invalid.'),
            params={'vin': vin},
        )
    if len(vin) != 17:
        raise ValidationError(
            _('VIN is too short.'),
            params={'vin': vin},
        )
    if not vin.isalnum():
        raise ValidationError(
            _('VIN should contain only letters and numbers.'),
            params={'vin': vin},
        )


def validate_year(prod_year):
    """
    Validate the production year. The production year can't be before 1886 when the first car was made.
    (Mercedes-Benz was the first to build a car in 1886.)

    Parameters:
        prod_year:

    Returns:
        None
    """
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
    """
    Validate the mileage. The mileage can't be more than 1 000 000 km.

    Parameters:
        mileage:

    Returns:
        None
    """
    if mileage > 1000000:
        raise ValidationError(
            _('You can\'t add the car with more than 1 000 000 km.'),
            params={'mileage': mileage},
        )


def past_rent(rent_date):
    """
    Validate the rent date. The rent date can't be in the past.

    Parameters:
        rent_date:

    Returns:
        None
    """
    if rent_date < date.today():
        raise ValidationError(
            _('Enter a valid date.'),
            params={'rent_date': rent_date},
        )


def future_rent(rent_date):
    """
    Validate the rent date. The rent date can't be more than two weeks in advance.

    Parameters:
        rent_date:

    Returns:
        None
    """
    two_weeks = timedelta(days=14)
    if rent_date > date.today() + two_weeks:
        raise ValidationError(
            _('You can rent a car for a maximum of two weeks in advance.'),
            params={'rent_date': rent_date},
        )
