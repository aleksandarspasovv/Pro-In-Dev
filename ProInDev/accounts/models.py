from datetime import date, timedelta, datetime

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    bio = models.TextField(
        blank=True,
        null=True
    )
    profile_image = CloudinaryField(
        'image',
        blank=True,
        null=True,
    )

    ROLE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    change_count = models.IntegerField(
        default=0,
    )

    last_change_date = models.DateTimeField(
        default=date.today,
    )

    github = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )

    instagram = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )

    def can_change_profile_image(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())

        if self.last_change_date and self.last_change_date.date() < start_of_week:
            self.change_count = 0

        if self.change_count >= 3:
            return False

        return True

    def __str__(self):
        return self.user.username
