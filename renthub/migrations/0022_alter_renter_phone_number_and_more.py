# Generated by Django 5.1.2 on 2024-11-30 05:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0021_rename_thai_citizenship_id_card_renter_thai_citizenship_id_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number can only contain numbers.', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='renter',
            name='thai_citizenship_id',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Citizenship ID can only contain numbers.', regex='^\\d+$')]),
        ),
    ]