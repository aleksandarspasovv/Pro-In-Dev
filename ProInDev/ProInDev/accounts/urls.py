# accounts/urls.py
from django.urls import path
from ProInDev.accounts.views import RegisterView, LoginView, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]
