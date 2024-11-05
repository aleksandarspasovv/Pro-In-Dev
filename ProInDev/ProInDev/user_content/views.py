from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ProInDev.user_content.forms import UserPostForm
from ProInDev.user_content.models import UserPost


class UserPostListView(LoginRequiredMixin, ListView):
    model = UserPost
    template_name = 'user_content/user_post_list.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user).order_by('-created_at')


class UserPostCreateView(LoginRequiredMixin, CreateView):
    model = UserPost
    form_class = UserPostForm
    template_name = 'user_content/user_post_form.html'
    success_url = reverse_lazy('user-post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserPostUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPost
    form_class = UserPostForm
    template_name = 'user_content/user_post_form.html'
    success_url = reverse_lazy('user-post-list')

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)


class UserPostDeleteView(LoginRequiredMixin, DeleteView):
    model = UserPost
    template_name = 'user_content/user_post_confirm_delete.html'
    success_url = reverse_lazy('user-post-list')

    def get_queryset(self):
        return UserPost.objects.filter(author=self.request.user)
