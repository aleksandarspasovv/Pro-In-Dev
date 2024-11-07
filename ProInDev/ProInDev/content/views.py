# content/views.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from ProInDev.content.models import Content, Post, Comment
from ProInDev.content.forms import ContentForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ContentListView(ListView):
    model = Content
    template_name = 'blog.html'
    context_object_name = 'contents'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Content.objects.all().order_by('-created_at')
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            return Content.objects.filter(author=admin_user).order_by('-created_at')
        return Content.objects.none()


@method_decorator(login_required, name='dispatch')
class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('content-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    return redirect('post-detail', pk=post.pk)


class ContentCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'author', 'image']  # Removed 'visibility'
    template_name = 'create-post.html'
    success_url = reverse_lazy('post_list')
