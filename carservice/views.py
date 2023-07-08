from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Car, Offer, Rent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from . forms import CarUpdateForm, CarDeleteForm, OfferUpdateForm, OfferDeleteForm
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from . forms import CarUpdateForm, CarDeleteForm, OfferUpdateForm, OfferDeleteForm, RentUpdateForm, RentDeleteForm
from django.views.generic import DeleteView
from django import forms


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['car_photo', 'vin', 'car_mileage', 'car_brand', 'car_model', 'date_of_prod']
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
    success_url = reverse_lazy('car_read')
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(instance=car)
        return render(request, 'car_update.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarUpdateForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_read')
        return render(request, 'car_update.html', {'form': form, 'car': car})


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('car_read')
    template_name = 'car_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


@login_required
def carsearch(request):
    search = request.GET.get('search')
    offers = Offer.objects.none()

    if search:
        search_terms = search.split()
        car_brand = ''
        car_model = ''

        if len(search_terms) > 0:
            car_brand = search_terms[0]
            if len(search_terms) > 1:
                car_model = search_terms[1]

        if car_brand and car_model:
            offers = Offer.objects.filter(Q(car__car_brand__iexact=car_brand) & Q(car__car_model__iexact=car_model))
        elif car_brand:
            offers = Offer.objects.filter(Q(car__car_brand__iexact=car_brand) | Q(car__car_model__iexact=car_brand))
        else:
            offers = Offer.objects.filter(Q(car__car_model__iexact=car_model))

    context = {
        'offers': offers,
        'search': search
    }
    return render(request, 'car_search.html', context)


@login_required
def offer_result(request, car_id, offer_id):
    car = get_object_or_404(Car, pk=car_id)
    offer = get_object_or_404(Offer, pk=offer_id)
    context = {'car': car, 'offer': offer}
    return render(request, 'offer_result.html', context)


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    fields = ['description', 'price']
    template_name = 'offer_create.html'
    success_url = reverse_lazy('offer_read')

    def form_valid(self, form):
        car_id = self.request.POST.get('car')
        car = get_object_or_404(Car, pk=car_id, user=self.request.user)
        form.instance.car = car
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['car'] = forms.ModelChoiceField(queryset=Car.objects.filter(user=self.request.user, offer__isnull=True))
        return form


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
            context={'offers': offers}
        )


class OfferUpdateView(LoginRequiredMixin, View):
    success_url = reverse_lazy('offer_read')

    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        form = OfferUpdateForm(instance=offer)
        return render(request, 'offer_update.html', {'form': form, 'offer': offer})

    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        form = OfferUpdateForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, 'offer_update.html', {'form': form, 'offer': offer})


class OfferDeleteView(LoginRequiredMixin, DeleteView):
    model = Offer
    success_url = reverse_lazy('offer_read')
    template_name = 'offer_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class RentCreateView(LoginRequiredMixin, CreateView):
    model = Rent
    fields = ['rent_start', 'duration']
    template_name = 'rent_create.html'
    success_url = reverse_lazy('rent_panel')

    def get_initial(self):
        initial = super().get_initial()
        initial['rent_start'] = now()
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        offer_id = self.kwargs['offer_id']
        offer = get_object_or_404(Offer, id=offer_id)

        if offer.user == self.request.user:
            return self.cannot_rent_own_car_response(offer)

        if Rent.objects.filter(offer=offer, status__in=['Rent active', 'pending']).exists():
            return self.offer_already_rented_response(offer)

        form.instance.offer = offer
        return super().form_valid(form)

    def cannot_rent_own_car_response(self, offer):
        context = {
            'message': 'You cannot rent your own car.',
            'offer': offer,
        }
        return self.render_to_response(self.get_context_data(**context))

    def offer_already_rented_response(self, offer):
        context = {
            'message': 'This offer is already rented.',
            'offer': offer,
        }
        return self.render_to_response(self.get_context_data(**context))


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


@login_required
def all_offers(request):
    offers = Offer.objects.exclude(user=request.user).exclude(rent__status='Rent active').exclude(rent__status='pending')
    return render(request, 'all_offers.html', {'offers': offers})


@login_required()
def rent_panel(request):
    user = request.user
    rents_as_owner = Rent.objects.filter(offer__user=user, close_rent=False)
    rents_as_renter = Rent.objects.filter(user=user, close_rent=False)
    return render(request, 'rent_panel.html', {'rents_as_owner': rents_as_owner, 'rents_as_renter': rents_as_renter})


@login_required
def rent_detail(request, rent_id):
    rent = get_object_or_404(Rent, id=rent_id)
    offer = rent.offer
    return render(request, 'rent_detail.html', {'rent': rent, 'offer': offer})


@login_required
def offer_detail(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    return render(request, 'offer_detail.html', {'offer': offer})


@login_required
def offer_detail_search(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    return render(request, 'offer_detail_search.html', {'offer': offer})


@login_required
def close_rent(request, rent_id):
    rent = get_object_or_404(Rent, id=rent_id)
    rent.close_rent = True
    rent.save()
    return redirect('rent_panel')


@login_required
def rent_archive(request):
    user = request.user

    rents_as_owner = Rent.objects.filter(offer__user=user, close_rent=True, status='Rent finished')
    rents_as_renter = Rent.objects.filter(user=user, close_rent=True, status='Rent finished')

    return render(request, 'rent_archive.html', {'rents_as_owner': rents_as_owner, 'rents_as_renter': rents_as_renter})
