from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static

from carservice.views import (
    CarCreateView, CarReadView, OfferReadView, OfferCreateView, RentCreateView, CarUpdateView,
    CarDeleteView, OfferUpdateView, OfferDeleteView, RentUpdateView, RentDeleteView, carsearch,
    offer_result, all_offers, rent_panel, rent_detail, offer_detail, offer_detail_search, close_rent, rent_archive
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('carsearch', carsearch, name='carsearch'),
    path('all_offers', all_offers, name='all_offers'),
    path('users/', include('users.urls')),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/read/', CarReadView.as_view(), name='car_read'),
    path('car/update/<int:car_id>/', CarUpdateView.as_view(), name='update_car'),
    path('car/delete/<int:pk>/', CarDeleteView.as_view(), name='delete_car'),
    path('offer/create/', OfferCreateView.as_view(), name='offer_create'),
    path('offer/read/', OfferReadView.as_view(), name='offer_read'),
    path('offer/result/<int:car_id>/<int:offer_id>/', offer_result, name='offer_result'),
    path('offer/update/<int:offer_id>/', OfferUpdateView.as_view(), name='offer_update'),
    path('offer/delete/<int:pk>/', OfferDeleteView.as_view(), name='offer_delete'),
    path('rent/create/<int:offer_id>/', RentCreateView.as_view(), name='rent_create'),
    path('rent_panel', rent_panel, name='rent_panel'),
    path('rent/update/<int:rent_id>/', RentUpdateView.as_view(), name='rent_update'),
    path('rent/delete/', RentDeleteView.as_view(), name='rent_delete'),
    path('rent_detail/<int:rent_id>/', rent_detail, name='rent_detail'),
    path('offer_detail/<int:offer_id>/', offer_detail, name='offer_detail'),
    path('offer_detail_search/<int:offer_id>/', offer_detail_search, name='offer_detail_search'),
    path('close_rent/<int:rent_id>/', close_rent, name='close_rent'),
    path('rent_archive/', rent_archive, name='rent_archive'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
