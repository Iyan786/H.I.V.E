# Generated by Django 5.1.4 on 2025-03-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0022_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
