from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approved']
    list_filter = ['approved']
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)

    approve_posts.short_description = "Approve selected posts"
