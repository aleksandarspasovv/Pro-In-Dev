from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approved']
    list_filter = ['approved']
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)

    approve_posts.short_description = "Approve selected posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['author__username', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"
