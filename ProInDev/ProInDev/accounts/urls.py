from django.urls import path
from .views import RegisterView, LoginView, profile_view, profile_edit, remove_account, change_password, \
    profile_view_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('remove_account/', remove_account, name='remove_account'),
    path('password_change/', change_password, name='change_password'),
    path('profile/<int:user_id>/', profile_view_user, name='profile'),
]
