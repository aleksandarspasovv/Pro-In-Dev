# content/views.py
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from ProInDev.content.models import Content, Post, Comment
from ProInDev.content.forms import ContentForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ContentListView(ListView):
    model = Post  # Make sure to pull from the Post model if that is the intended blog content
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all().order_by('-created_at')
        return Post.objects.none()


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


@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user.username
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('post-detail', args=[post.pk])))
    return HttpResponseRedirect(reverse_lazy('post-detail', args=[post.pk]))


class ContentCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image']  # Removed 'visibility'
    template_name = 'create-post.html'
    success_url = reverse_lazy('content-list')
