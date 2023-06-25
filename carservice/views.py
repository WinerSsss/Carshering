from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car, Offer, Rent


from django.utils import timezone

from . forms import CarUpdateForm, CarDeleteForm, OfferUpdateForm, OfferDeleteForm


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['serial_number', 'car_mileage', 'car_model', 'car_year']
    template_name = 'car_create.html'
    success_url = reverse_lazy('car_read')


class CarReadView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request, template_name='car_read.html',
            context={'cars': Car.objects.all()}
        )

class CarUpdateView(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(instance=car)
        return render(request, 'car_update.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('/car/read/')
        return render(request, 'car_update.html', {'form': form, 'car': car})


class CarDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        cars = Car.objects.all()
        form = CarDeleteForm()
        return render(request, 'car_delete.html', {'form': form, 'cars': cars})

    def post(self, request):
        form = CarDeleteForm(request.POST)
        if form.is_valid():
            car_id = form.cleaned_data['car']
            car = Car.objects.get(id=car_id)
            car.delete()
            return redirect('/car/read/')
        return render(request, 'car_delete.html', {'form': form})


class OfferCreateView(LoginRequiredMixin, CreateView):
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

class OfferUpdateView(LoginRequiredMixin, View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        form = OfferUpdateForm(instance=offer)
        return render(request, 'offer_update.html', {'form': form, 'offer': offer})

    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        form = OfferUpdateForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('/offer/read/')
        return render(request, 'offer_update.html', {'form': form, 'offer': offer})


class OfferDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        offers = Offer.objects.all()
        form = OfferDeleteForm()
        return render(request, 'offer_delete.html', {'form': form, 'offers': offers})

    def post(self, request):
        form = OfferDeleteForm(request.POST)
        if form.is_valid():
            offer_id = form.cleaned_data['offer']
            offer = Offer.objects.get(id=offer_id)
            offer.delete()
            return redirect('/offer/read/')
        return render(request, 'offer_delete.html', {'form': form})


class RentCreateView(CreateView):
    model = Rent
    fields = ['status', 'rent_start', 'rent_stop', 'offer', 'user']
    template_name = 'rent_create.html'
    success_url = reverse_lazy('rent_read')


class RentListView(View):
    def get(self, request):
        rents = Rent.objects.all()

        return render(
            request,
            template_name='rent_read.html',
            context={'rents': rents}
        )