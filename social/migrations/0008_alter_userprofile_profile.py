# Generated by Django 5.1.4 on 2025-02-04 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_remove_userprofile_image_userprofile_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
