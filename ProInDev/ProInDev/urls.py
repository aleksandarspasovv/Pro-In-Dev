# ProInDev/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ProInDev.public.urls')),  # Public app at root URL
    path('accounts/', include('ProInDev.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('content/', include('ProInDev.content.urls')),
    path('user_content', include('ProInDev.user_content.urls')),
]
