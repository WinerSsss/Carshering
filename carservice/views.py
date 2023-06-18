from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from carservice.models import Car, Offer


class CarCreateView(CreateView):
    model = Car
    fields = ['serial_number', 'car_mileage', 'car_model', 'car_year']
    template_name = 'car_create.html'
    success_url = '/car/read'


class CarReadView(View):
    def get(self, request):
        return render(
            request, template_name='car_read.html',
            context={'cars': Car.objects.all()}
        )

class OfferCreateView(CreateView):
    model = Offer
    fields = ['car', 'description', 'price']
    template_name = 'offer_create.html'
    success_url = '/offer/read/'


class OfferReadView(View):
    def get(self, request):
        return render(
            request, template_name='offer_read.html',
            context={'offers': Offer.objects.all()}
        )
