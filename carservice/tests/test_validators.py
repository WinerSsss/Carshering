from django.test import TestCase

from carservice import validators


class TestVinValidator(TestCase):
    def test_vin_validator(self):
        self.assertTrue(validators.vin_validator('JH4DB1550LS000111'))
        self.assertTrue(validators.vin_validator('5NPEB4AC1DH576656'))
        self.assertTrue(validators.vin_validator('1G1JC1240WM100000'))
        self.assertTrue(validators.vin_validator('1G1JC1240WM100000'))
        self.assertFalse(validators.vin_validator('1G1JC1240WM10000'))
        self.assertFalse(validators.vin_validator('1G1JC1240WM1000000'))
        self.assertFalse(validators.vin_validator('1G1JC1240WM10000A'))
        self.assertFalse(validators.vin_validator('1G1JC1240WM10000a'))
