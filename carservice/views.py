from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Car, Offer, Rent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from . forms import CarUpdateForm, CarDeleteForm, OfferUpdateForm, OfferDeleteForm
from django.core.files.storage import FileSystemStorage


from . forms import CarUpdateForm, CarDeleteForm, OfferUpdateForm, OfferDeleteForm, RentUpdateForm, RentDeleteForm

class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['car_photo', 'serial_number', 'car_mileage', 'car_brand', 'car_model', 'date_of_prod']
    template_name = 'car_create.html'
    success_url = reverse_lazy('car_read')

    def get_initial(self):
        initial = super().get_initial()
        initial['date_of_prod'] = 'YYYY-MM-DD'
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        car_photo = form.cleaned_data['car_photo']
        photo_save = FileSystemStorage()
        photo_name = photo_save.save(car_photo.name, car_photo)
        car_photo_url = photo_save.url(photo_name)
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


class CarUpdateView(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(instance=car)
        return render(request, 'car_update.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(request.POST, request.FILES, instance=car)
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


class RentListView(View):

    def get(self, request):
        rents = self.get_queryset()

        return render(
            request,
            template_name='rent_read.html',
            context={'rents': rents}
        )


class RentUpdateView(LoginRequiredMixin, View):
    def get(self, request, rent_id):
        rent = get_object_or_404(Rent, id=rent_id)
        form = RentUpdateForm(instance=rent)
        return render(request, 'rent_update.html', {'form': form, 'rent': rent})

    def post(self, request, rent_id):
        rent = get_object_or_404(Rent, id=rent_id)
        form = RentUpdateForm(request.POST, instance=rent)
        if form.is_valid():
            form.save()
            return redirect('rent_read')
        return render(request, 'rent_update.html', {'form': form, 'rent': rent})


class RentDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        form = RentDeleteForm(user=request.user)
        return render(request, 'rent_delete.html', {'form': form})

    def post(self, request):
        form = RentDeleteForm(request.user, request.POST)
        if form.is_valid():
            rent = form.cleaned_data['rent']
            rent.delete()
            return redirect('rent_read')
        return render(request, 'rent_delete.html', {'form': form})