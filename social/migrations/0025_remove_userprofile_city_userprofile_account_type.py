# Generated by Django 5.1.4 on 2025-04-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0024_post_disliked_by_post_liked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='city',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=10),
        ),
    ]
