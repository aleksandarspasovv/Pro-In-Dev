# public/urls.py
from django.urls import path
from ProInDev.public import views

urlpatterns = [
    path('', views.index, name='index'),  # Landing page
    path('privacy-and-terms/', views.privacy_and_terms, name='privacy-and-terms'),
    path('help/', views.help_view, name='help'),
]
