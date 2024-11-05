from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    media = models.ImageField(upload_to='user_content/media/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')

    def __str__(self):
        return self.title
