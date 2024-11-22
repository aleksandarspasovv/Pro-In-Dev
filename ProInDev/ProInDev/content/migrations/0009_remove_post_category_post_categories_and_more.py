# Generated by Django 4.2.16 on 2024-11-22 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_category_post_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='posts', to='content.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Programming', 'Programming'), ('Jobs', 'Jobs'), ('Tutorials', 'Tutorials'), ('News', 'News'), ('Other', 'Other')], max_length=100, unique=True),
        ),
    ]
