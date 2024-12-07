# Generated by Django 4.2.16 on 2024-12-01 04:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='change_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_change_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]