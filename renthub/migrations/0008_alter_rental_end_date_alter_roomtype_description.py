# Generated by Django 5.1.2 on 2024-11-08 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0007_rental_is_paid_rental_last_checked_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 8, 14, 35, 8, 98057, tzinfo=datetime.timezone.utc), verbose_name='date checkout'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
