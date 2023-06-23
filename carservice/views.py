from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from . models import Car, Offer, Rent
from django.utils import timezone
from .forms import CarUpdateForm, CarDeleteForm, OfferPriceModifyForm, CarAccessoriesForm


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


class OfferPriceModify(View):
    def get(self, request):
        offers = Offer.objects.all()
        form = OfferPriceModifyForm()
        return render(request, 'offer_price_update.html', {'form': form, 'offers': offers})
    def post(self, request):
        if request.method == "POST":
            form = OfferPriceModifyForm(request.POST)
            if form.is_valid():
                offer_id = request.POST.get('offer')
                new_price = form.cleaned_data['price']
                offer = Offer.objects.get(id=offer_id)
                offer.price = new_price
                offer.save()
                return redirect('/offer/read/')
            offers = Offer.objects.all()
            return render(request,'offer_price_update.html',{'form': form,'offers': offers})
class CarUpdate(View):
    def get(self, request):
        form = CarUpdateForm()
        return render(request, 'car_update.html', {'form': form})

    def post(self,request):
        form = CarUpdateForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect('/car/read/')
        return render(request,'car_modify.html',{'form': form})


class CarDelete(View):
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

class CarAccessoriesView(View):
    def get(self, request):
        form = CarAccessoriesForm()
        return render(request, 'car_accessories_choice.html', {'form': form})

    def post(self, request):
        form = CarAccessoriesForm(request.POST)
        if form.is_valid():
            selected_accessories = form.cleaned_data['accessories']
            request.session['selected_accessories'] = selected_accessories
            return redirect('/car/car_accessories_summary')
        return render(request, 'car_accessories_choice.html', {'form': form})

class CarAccessoriesSummaryView(View):
    def get(self, request):
        accessories = request.session.get('selected_accessories', [])
        return render(request, 'car_accessories_summary.html', {'accessories': accessories})