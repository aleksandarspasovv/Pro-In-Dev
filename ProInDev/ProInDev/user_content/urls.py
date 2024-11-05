# user_content/urls.py
from django.urls import path
from ProInDev.user_content.views import UserPostListView, UserPostCreateView, UserPostUpdateView, UserPostDeleteView

urlpatterns = [
    path('', UserPostListView.as_view(), name='user-post-list'),
    path('new/', UserPostCreateView.as_view(), name='user-post-create'),
    path('<int:pk>/edit/', UserPostUpdateView.as_view(), name='user-post-edit'),
    path('<int:pk>/delete/', UserPostDeleteView.as_view(), name='user-post-delete'),
]
