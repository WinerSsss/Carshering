from .models import Car, Offer, Rent
from django import forms


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['vin', 'car_mileage', 'car_brand', 'car_model', 'date_of_prod', 'car_photo']


class OfferUpdateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['description', 'price']


class RentUpdateForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['rent_start', 'duration']


class RentDeleteForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(RentDeleteForm, self).__init__(*args, **kwargs)
        self.fields['rent'].queryset = Rent.objects.filter(user=user)

    rent = forms.ModelChoiceField(queryset=Rent.objects.none())


class UpdateStatusForm(forms.Form):
    pass
