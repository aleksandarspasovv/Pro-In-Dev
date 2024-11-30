from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CategoryInline(admin.TabularInline):
    model = Post.categories.through
    extra = 1


from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'approved', 'has_pending_update', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    actions = ['approve_posts', 'approve_updates', 'reject_updates']  # Ensure these actions are included
    readonly_fields = ['pending_update_display']

    def has_pending_update(self, obj):
        return bool(obj.pending_update)

    has_pending_update.boolean = True
    has_pending_update.short_description = "Pending Update"

    def pending_update_display(self, obj):
        if obj.pending_update:
            return f"Title: {obj.pending_update.get('title', 'N/A')}\nBody: {obj.pending_update.get('body', 'N/A')}"
        return "No pending update"

    pending_update_display.short_description = "Pending Update Details"

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected posts have been approved.")

    approve_posts.short_description = "Approve selected posts"

    def approve_updates(self, request, queryset):
        for post in queryset.filter(pending_update__isnull=False):
            post.approve_update()
        self.message_user(request, "Selected post updates have been approved.")

    approve_updates.short_description = "Approve selected updates"

    def reject_updates(self, request, queryset):
        queryset.update(pending_update=None)
        self.message_user(request, "Selected post updates have been rejected.")

    reject_updates.short_description = "Reject selected updates"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['author__username', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"
