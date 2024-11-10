from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from ProInDev.user_content.forms import UserPostForm
# from ProInDev.user_content.forms import UserPostForm
from ProInDev.user_content.models import UserPost


class UserPostListView(LoginRequiredMixin, ListView):
    model = UserPost
    template_name = 'blog.html'  # Make sure this points to blog.html
    context_object_name = 'user_posts'  # Use 'user_posts' to match the template

    paginate_by = 10

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user).order_by('-created_at')

class UserPostCreateView(LoginRequiredMixin, CreateView):
    model = UserPost
    form_class = UserPostForm
    template_name = 'user_post_form.html'
    success_url = reverse_lazy('user-post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       "There was an error in creating your post. Please ensure it meets all requirements.")
        return super().form_invalid(form)


class UserPostUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPost
    form_class = UserPostForm
    template_name = 'user_post_form.html'
    success_url = reverse_lazy('user-post-list')

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       "There was an error in updating your post. Please ensure it meets all requirements.")
        return super().form_invalid(form)


class UserPostDeleteView(LoginRequiredMixin, DeleteView):
    model = UserPost
    template_name = 'user_post_confirm_delete.html'
    success_url = reverse_lazy('user-post-list')

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)
