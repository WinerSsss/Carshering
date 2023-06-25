from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Register, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomPasswordResetDoneView
from users.views import profile, EditProfile

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

    path('profile/', profile, name='profile'),
    path('profile/edit/', EditProfile.as_view(), name='edit_profile'),
]