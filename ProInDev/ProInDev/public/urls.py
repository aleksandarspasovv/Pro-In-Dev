# public/urls.py
from django.urls import path
from ProInDev.public import views

urlpatterns = [
    path('', views.index, name='index'),  # Landing page
    path('about/', views.about, name='about'),
    path('help/', views.help_view, name='help'),
]
