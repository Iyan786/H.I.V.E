# Generated by Django 5.1.4 on 2025-02-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_alter_userprofile_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]
