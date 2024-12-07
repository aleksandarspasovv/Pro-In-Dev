from datetime import date, timedelta, datetime
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
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
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

        # Get today's date
        today = datetime.now().date()
        # Calculate the start of the current week (Monday)
        start_of_week = today - timedelta(days=today.weekday())

        # Reset change_count if last change was before the current week
        if self.last_change_date and self.last_change_date.date() < start_of_week:
            self.change_count = 0

        # Deny changes if the limit of 3 changes per week is reached
        if self.change_count >= 3:
            return False

        return True

