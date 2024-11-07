from django.urls import path
from ProInDev.accounts.views import RegisterView, LoginView, profile_view, profile_edit
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('settings/', profile_edit, name='settings'),  # Alias for the settings page
]
