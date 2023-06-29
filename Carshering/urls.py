from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static

from carservice.views import CarCreateView, CarReadView, OfferReadView, OfferCreateView, RentCreateView, RentListView, \
    CarUpdateView, CarDeleteView, OfferUpdateView, OfferDeleteView, RentUpdateView, RentDeleteView, carsearch, offer_result


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('carsearch', carsearch, name='carsearch'),

    path('users/', include('users.urls')),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/read/', CarReadView.as_view(), name='car_read'),
    path('car/update/<int:car_id>/', CarUpdateView.as_view(), name='update_car'),
    path('car/delete/', CarDeleteView.as_view(), name='delete_car'),
    path('offer/create/', OfferCreateView.as_view()),
    path('offer/read/', OfferReadView.as_view(), name='offer_read'),
    path('offer/result/<int:car_id>/<int:offer_id>/', offer_result, name='offer_result'),
    path('offer/update/<int:offer_id>/', OfferUpdateView.as_view(), name='offer_read'),
    path('offer/delete/', OfferDeleteView.as_view(), name='offer_car'),
    path('rent/create/', RentCreateView.as_view()),
    path('rent/read/', RentListView.as_view(), name='rent_read'),

    path('rent/update/<int:rent_id>/',RentUpdateView.as_view(),name='rent_update'),
    path('rent/delete/', RentDeleteView.as_view(), name='rent_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
