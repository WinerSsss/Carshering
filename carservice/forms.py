from . models import Car, Offer
from django import forms


class CarUpdateForm(forms.ModelForm):
    car_choice = forms.ModelChoiceField(queryset=Car.objects.all(), empty_label=None)

    class Meta:
        model = Car
        fields = ['serial_number', 'car_mileage', 'car_model','car_year']

class CarDeleteForm(forms.Form):
    car = forms.ChoiceField(label='Car')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].choices = [(car.id, str(car)) for car in Car.objects.all()]

class OfferPriceModifyForm(forms.ModelForm):
    offer_choice = forms.ModelChoiceField(queryset=Offer.objects.all(), empty_label=None)
    class Meta:
        model = Offer
        fields = ['price']


class CarAccessoriesForm(forms.Form):
    SEAT_CHILD = 'seat_child'
    GPS = 'gps'
    ROOF_RACK = 'roof_rack'

    ACCESSORY_CHOICE = (
        (SEAT_CHILD, 'Child seat'),
        (GPS, 'GPS'),
        (ROOF_RACK, 'Roof rack'),
    )

    accessories = forms.MultipleChoiceField(
        choices=ACCESSORY_CHOICE,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )