from django import forms
from carservice import models

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = '__all__'