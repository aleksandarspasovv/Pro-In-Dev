from django.urls import path
from ProInDev.content.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, approve_post

urlpatterns = [
    path('', PostListView.as_view(), name='content-list'),
    path('new/', PostCreateView.as_view(), name='create-post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/approve/', approve_post, name='post-approve'),
]
