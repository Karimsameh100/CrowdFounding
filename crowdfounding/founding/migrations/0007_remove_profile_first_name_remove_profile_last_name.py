# Generated by Django 5.1 on 2024-08-30 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('founding', '0006_rename_firse_name_profile_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
