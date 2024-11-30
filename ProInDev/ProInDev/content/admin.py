from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CategoryInline(admin.TabularInline):
    model = Post.categories.through
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approved', 'get_categories', 'created_at']
    list_filter = ['approved', 'categories', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    actions = ['approve_posts']
    inlines = [CategoryInline]  # Add the inline

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"

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
