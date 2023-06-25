from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import profile, edit_profile
from django.conf.urls.static import static
from carservice.views import CarCreateView, CarReadView, OfferReadView, OfferCreateView, RentCreateView, RentListView, CarUpdateView, CarDeleteView, OfferUpdateView, OfferDeleteView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('users/', include('users.urls')),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/read/', CarReadView.as_view(), name='car_read'),
    path('car/update/<int:car_id>/', CarUpdateView.as_view(), name='update_car'),
    path('car/delete/', CarDeleteView.as_view(), name='delete_car'),
    path('offer/create/', OfferCreateView.as_view()),
    path('offer/read/', OfferReadView.as_view(), name='offer_read'),
    path('offer/update/<int:offer_id>/', OfferUpdateView.as_view(), name='offer_read'),
    path('offer/delete/', OfferDeleteView.as_view(), name='offer_car'),
    path('rent/create/', RentCreateView.as_view()),
    path('rent/read/', RentListView.as_view(), name='rent_read'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
