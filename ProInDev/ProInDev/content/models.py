from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Content(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self):
        return self.title
