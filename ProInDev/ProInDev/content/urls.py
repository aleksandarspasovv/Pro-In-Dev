# content/urls.py
from django.urls import path
from ProInDev.content.views import ContentListView, ContentCreateView, ContentDetailView, ContentUpdateView, ContentDeleteView

urlpatterns = [
    path('', ContentListView.as_view(), name='content-list'),
    path('new/', ContentCreateView.as_view(), name='content-create'),
    path('<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
    path('<int:pk>/edit/', ContentUpdateView.as_view(), name='content-edit'),
    path('<int:pk>/delete/', ContentDeleteView.as_view(), name='content-delete'),
]
