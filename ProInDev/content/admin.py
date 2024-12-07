from django.contrib import admin
from .models import Post, Comment, Category


# Admin configuration for the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Display the name of the category in the admin list view
    list_display = ['name']
    # Enable search functionality for the name field
    search_fields = ['name']


# Inline configuration to manage categories in the Post admin
class CategoryInline(admin.TabularInline):
    # Specifies the model relation to display
    model = Post.categories.through
    # Adds one empty form for adding categories
    extra = 1


# Admin configuration for the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ['title', 'author', 'approved', 'has_pending_update', 'created_at']
    # Filters for the list view
    list_filter = ['approved', 'created_at']
    # Enable search functionality for specified fields
    search_fields = ['title', 'body', 'author__username']
    # Custom actions available in the admin
    actions = ['approve_posts', 'approve_updates', 'reject_updates']
    # Fields that are read-only in the admin
    readonly_fields = ['pending_update_display']

    # Displays whether a post has a pending update
    def has_pending_update(self, obj):
        return bool(obj.pending_update)

    has_pending_update.boolean = True
    has_pending_update.short_description = "Pending Update"

    # Displays details of the pending update
    def pending_update_display(self, obj):
        if obj.pending_update:
            return f"Title: {obj.pending_update.get('title', 'N/A')}\nBody: {obj.pending_update.get('body', 'N/A')}"
        return "No pending update"

    pending_update_display.short_description = "Pending Update Details"

    # Approves selected posts
    def approve_posts(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected posts have been approved.")

    approve_posts.short_description = "Approve selected posts"

    # Approves pending updates for selected posts
    def approve_updates(self, request, queryset):
        for post in queryset.filter(pending_update__isnull=False):
            post.approve_update()
        self.message_user(request, "Selected post updates have been approved.")

    approve_updates.short_description = "Approve selected updates"

    # Rejects pending updates for selected posts
    def reject_updates(self, request, queryset):
        queryset.update(pending_update=None)
        self.message_user(request, "Selected post updates have been rejected.")

    reject_updates.short_description = "Reject selected updates"


# Admin configuration for the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ['post', 'author', 'content', 'approved', 'created_at']
    # Filters for the list view
    list_filter = ['approved', 'created_at']
    # Enable search functionality for specified fields
    search_fields = ['author__username', 'content']
    # Custom actions available in the admin
    actions = ['approve_comments']

    # Approves selected comments
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"
