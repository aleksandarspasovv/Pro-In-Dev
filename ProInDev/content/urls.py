from django.urls import path
from ProInDev.content.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, \
    approve_post, post_comment, like_post, like_comment, approve_comment, post_edit_inline, post_delete_inline

urlpatterns = [
    path('', PostListView.as_view(), name='content-list'),
    path('new/', PostCreateView.as_view(), name='create-post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/approve/', approve_post, name='post-approve'),
    path('<int:pk>/like/', like_post, name='like-post'),
    path('comment/<int:comment_id>/like/', like_comment, name='like-comment'),
    path('<int:pk>/comment/', post_comment, name='post-comment'),
    path('comment/<int:comment_id>/approve/', approve_comment, name='approve-comment'),
    path('<int:pk>/edit-inline/', post_edit_inline, name='post-edit-inline'),
    path('<int:pk>/delete-inline/', post_delete_inline, name='post-delete-inline'),
]
