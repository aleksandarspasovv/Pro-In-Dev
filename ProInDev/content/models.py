from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Programming', 'Programming'),
        ('Jobs', 'Jobs'),
        ('Tutorials', 'Tutorials'),
        ('News', 'News'),
        ('Other', 'Other'),
    ]

    name = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        unique=True,
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)

    body = models.TextField()

    media = CloudinaryField(
        'image'
        , blank=True,
        null=True,
    )

    created_at = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    approved = models.BooleanField(default=False)

    public = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True,
    )

    categories = models.ManyToManyField(
        Category,
        related_name="posts",
        blank=True,
    )

    pending_update = models.JSONField(
        blank=True,
        null=True,
    )

    def total_likes(self):
        return self.likes.count()

    def approve_update(self):
        if self.pending_update:
            self.title = self.pending_update.get('title', self.title)
            self.body = self.pending_update.get('body', self.body)
            self.pending_update = None
            self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        User,
        related_name="liked_comments",
        blank=True,
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
