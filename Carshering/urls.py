from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from carservice.views import CarCreateView, CarReadView, OfferReadView, OfferCreateView, RentCreateView, RentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('users/', include('users.urls')),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/read/', CarReadView.as_view(), name='car_read'),
    path('offer/create/', OfferCreateView.as_view()),
    path('offer/read/', OfferReadView.as_view(), name='offer_read'),
    path('rent/create/', RentCreateView.as_view()),
    path('rent/read/', RentListView.as_view(), name='rent_read'),
]
