# content/urls.py
from django.urls import path
from ProInDev.content.views import (
    ContentListView, ContentCreateView, PostDetailView, post_comment
)

urlpatterns = [
    path('', ContentListView.as_view(), name='content-list'),  # List of all content
    path('new/', ContentCreateView.as_view(), name='content-create'),  # Create new content
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Individual post detail
    path('post/<int:pk>/comment/', post_comment, name='post-comment'),  # Comment on a post
]