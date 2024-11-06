# content/urls.py
from django.urls import path
from ProInDev.content.views import ContentListView, ContentCreateView, PostDetailView, post_comment

urlpatterns = [
    path('', ContentListView.as_view(), name='content-list'),
    path('new/', ContentCreateView.as_view(), name='content-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/', post_comment, name='post-comment'),
]
