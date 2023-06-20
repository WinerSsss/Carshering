from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from Carshering.registration.models import User


class UserRegistrationView(CreateView):
    models = User
    template_name = 'user_registration.html'
    fields = '__all__'
    success_url = reverse_lazy('here_we_go')
