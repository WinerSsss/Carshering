from . models import Car, Offer
from django import forms



class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['serial_number', 'car_mileage', 'car_model', 'car_year']

class CarDeleteForm(forms.Form):
    car = forms.ChoiceField(label='Car')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].choices = [(car.id, str(car)) for car in Car.objects.all()]

class OfferUpdateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['description', 'price', 'car']

class OfferDeleteForm(forms.Form):
    offer = forms.ChoiceField(label='Offer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['offer'].choices = [(offer.id, str(offer)) for offer in Offer.objects.all()]