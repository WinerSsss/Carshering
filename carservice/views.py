from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy

from carservice.models import Car
from carservice.forms import CarForm


class CarCreateView(generic.FormView):
    template_name = 'car_form.html'
    form_class = CarForm
    success_url = reverse_lazy('car_form')


    def form_valid(self, form):
        ans = super().form_valid(form)
        oczyszczone = form.cleaned_data

        Car.objects.create(
            serial_number=oczyszczone['serial_number'],
            car_mileage=oczyszczone['car_mileage'],
            car_model=oczyszczone['car_model'],
            car_year=oczyszczone['car_year'],
        )

        return ans



