# Generated by Django 5.1.4 on 2025-02-05 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='photo',
        ),
    ]
