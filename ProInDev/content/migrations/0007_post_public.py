# Generated by Django 4.2.16 on 2024-11-13 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_comment_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]