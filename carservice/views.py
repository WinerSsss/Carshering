from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from carservice.models import Car, Offer, Rent
from django.utils import timezone


class CarCreateView(CreateView):
    model = Car
    fields = ['serial_number', 'car_mileage', 'car_model', 'car_year']
    template_name = 'car_create.html'
    success_url = reverse_lazy('car_read')


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
    success_url = reverse_lazy('offer_read')


class OfferReadView(View):
    def get(self, request):
        return render(
            request, template_name='offer_read.html',
            context={'offers': Offer.objects.all()}
        )


class RentCreateView(CreateView):
    model = Rent
    fields = ['status', 'rent_start', 'rent_stop', 'offer', 'user']
    template_name = 'rent_create.html'
    success_url = reverse_lazy('rent_read')


class RentListView(View):
    def get(self, request):
        rents = Rent.objects.all()
        rent_status = [rent.status_answer() for rent in rents]
        rent_start = [rent.rent_start for rent in rents]
        rent_stop = [rent.rent_stop for rent in rents]

        return render(
            request,
            template_name='rent_read.html',
            context={'rents': rents, 'rent_status': rent_status, 'rent_start': rent_start, 'rent_stop': rent_stop,}
        )