# Generated by Django 5.1.2 on 2024-11-30 04:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0018_alter_roomimage_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be exactly 10 digits.', regex='^\\d{10}$')]),
        ),
    ]