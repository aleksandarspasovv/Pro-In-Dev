from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from ProInDev.content.models import Post, Comment
from ProInDev.content.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'user_posts'
    paginate_by = 25

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')

        # Check if the user is authenticated and then access userprofile
        if self.request.user.is_authenticated:
            if not getattr(self.request.user, 'userprofile', None) or self.request.user.userprofile.role != 'admin':
                queryset = queryset.filter(approved=True)
        else:
            queryset = queryset.filter(approved=True)

        return queryset


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.approved = False
        messages.success(self.request, "Post created successfully and is awaiting approval.")
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit-post.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('post-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

@user_passes_test(lambda u: u.userprofile.role == 'admin')
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved = True
    post.save()
    messages.success(request, "The post has been approved.")
    return redirect('post-list')

@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('post-detail', args=[post.pk])))
    return HttpResponseRedirect(reverse('post-detail', args=[post.pk]))
