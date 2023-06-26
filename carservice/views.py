from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Car, Offer, Rent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from datetime import timedelta


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['serial_number', 'car_mileage', 'car_brand', 'car_model', 'date_of_prod']
    template_name = 'car_create.html'
    success_url = reverse_lazy('car_read')

    def get_initial(self):
        initial = super().get_initial()
        initial['date_of_prod'] = 'YYYY-MM-DD'
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CarReadView(LoginRequiredMixin, View):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Car.objects.all()
        else:
            return Car.objects.filter(user=self.request.user)

    def get(self, request):
        cars = self.get_queryset()
        return render(
            request, template_name='car_read.html',
            context={'cars': cars}
        )


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    fields = ['car', 'description', 'price']
    template_name = 'offer_create.html'
    success_url = reverse_lazy('offer_read')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OfferReadView(LoginRequiredMixin, View):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Offer.objects.all()
        else:
            return Offer.objects.filter(user=self.request.user)

    def get(self, request):
        offers = self.get_queryset()

        return render(
            request, template_name='offer_read.html',
            context={'offers': Offer.objects.all()}
        )


class RentCreateView(LoginRequiredMixin, CreateView):
    model = Rent
    fields = ['rent_start', 'duration', 'offer']
    template_name = 'rent_create.html'
    success_url = reverse_lazy('rent_read')

    def get_initial(self):
        initial = super().get_initial()
        initial['rent_start'] = now()
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RentListView(LoginRequiredMixin, View):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Rent.objects.all()
        else:
            return Rent.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request):
        rents = self.get_queryset()

        return render(
            request,
            template_name='rent_read.html',
            context={'rents': rents}
        )
      