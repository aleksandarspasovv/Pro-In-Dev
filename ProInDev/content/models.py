from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    CATEGORY_CHOICES = [  # Predefined choices for categories
        ('Programming', 'Programming'),
        ('Jobs', 'Jobs'),
        ('Tutorials', 'Tutorials'),
        ('News', 'News'),
        ('Other', 'Other'),
    ]

    name = models.CharField(  # Name of the category
        max_length=100,
        choices=CATEGORY_CHOICES,
        unique=True  # Ensure each category name is unique
    )

    def __str__(self):  # String representation of the category
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)  # Title of the post
    body = models.TextField()  # Content/body of the post
    media = models.ImageField(  # Optional media/image for the post
        upload_to='media/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(default=timezone.now)  # Post creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of the last update
    author = models.ForeignKey(  # Author of the post
        to=User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    approved = models.BooleanField(default=False)  # Whether the post is approved
    public = models.BooleanField(default=False)  # Whether the post is public
    likes = models.ManyToManyField(  # Users who liked the post
        User,
        related_name="liked_posts",
        blank=True
    )
    categories = models.ManyToManyField(  # Categories associated with the post
        Category,
        related_name="posts",
        blank=True
    )

    pending_update = models.JSONField(  # JSON field for pending updates
        blank=True,
        null=True
    )

    def total_likes(self):  # Returns the total number of likes
        return self.likes.count()

    def approve_update(self):  # Applies the pending update, if any
        if self.pending_update:
            self.title = self.pending_update.get('title', self.title)  # Update title
            self.body = self.pending_update.get('body', self.body)  # Update body
            self.pending_update = None  # Clear the pending update
            self.save()

    def __str__(self):  # String representation of the post
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(  # Post associated with the comment
        Post,
        related_name="comments",
        on_delete=models.CASCADE)

    author = models.ForeignKey(  # Author of the comment
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    approved = models.BooleanField(default=False)  # Whether the comment is approved
    likes = models.ManyToManyField(  # Users who liked the comment
        User,
        related_name="liked_comments",
        blank=True)

    def total_likes(self):  # Returns the total number of likes
        return self.likes.count()

    def __str__(self):  # String representation of the comment
        return f"Comment by {self.author} on {self.post}"
