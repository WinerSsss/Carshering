from django import forms
from carservice import models

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = '__all__'


class OfferForm(forms.ModelForm):
    class Meta:
        model = models.Offer
        fields = '__all__'
