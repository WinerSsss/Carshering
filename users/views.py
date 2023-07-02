from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .models import Profile
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdate


class EditProfile(LoginRequiredMixin, View):
    template_name = 'edit_profile.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdate(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
            'user_form': user_form,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully changed.')
            return redirect('profile')

        context = {
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, self.template_name, context)



@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


class Register(FormView):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password/password_reset_form.html'
    email_template_name = 'reset_password/password_reset_email.html'
    success_url = reverse_lazy('password_reset')
    form_class = PasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reset_password/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'reset_password/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'reset_password/password_reset_complete.html'


