from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import PostForm, CommentForm
from .models import Post, Comment, Category


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'user_posts'
    paginate_by = 25

    def get_queryset(self):
        queryset = Post.objects.filter(approved=True)
        category = self.request.GET.get('category', 'all')

        if category != 'all':
            queryset = queryset.filter(categories__name=category)

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['important_posts'] = Post.objects.filter(approved=True, public=True).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('content-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categories'].queryset = Category.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.approved = False
        form.save()
        form.instance.categories.set(form.cleaned_data['categories'])
        messages.success(self.request, "Post created successfully and is awaiting approval.")
        return super().form_valid(form)



class PostDetailView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
            context['comments'] = self.object.comments.filter(approved=True).order_by('-created_at')
        else:
            context['comments'] = None
        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit-post.html'
    success_url = reverse_lazy('content-list')

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('content-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved = True
    post.save()
    messages.success(request, "The post has been approved.")
    return redirect('content-list')


@user_passes_test(lambda u: u.is_superuser)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.approved = True
    comment.save()
    messages.success(request, "The comment has been approved.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('post-detail', args=[comment.post.pk])))


@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.approved = False
            comment.save()
            messages.success(request, "Comment submitted and awaiting approval.")
            return HttpResponseRedirect(reverse('content-list'))
        else:
            messages.error(request, "There was an error submitting your comment. Please try again.")
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('post-detail', args=[pk])))


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
