from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ProInDev.content.forms import ContentForm
from ProInDev.content.models import Content


class ContentListView(ListView):
    model = Content
    template_name = 'blog.html'
    context_object_name = 'contents'

    def get_queryset(self):
        return Content.objects.filter(visibility='public').order_by('-created_at')


class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'create-page.html'
    success_url = reverse_lazy('content-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContentDetailView(DetailView):
    model = Content
    template_name = 'post-details.html'
    context_object_name = 'content'


class ContentUpdateView(UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'create-page.html'
    success_url = reverse_lazy('content-list')


class ContentDeleteView(DeleteView):
    model = Content
    template_name = 'content_confirm_delete.html'
    success_url = reverse_lazy('content-list')
