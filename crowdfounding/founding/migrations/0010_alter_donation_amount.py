# Generated by Django 5.1 on 2024-09-05 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('founding', '0009_project_current_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
