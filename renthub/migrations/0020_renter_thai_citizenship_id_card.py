# Generated by Django 5.1.2 on 2024-11-30 04:39

import renthub.models.renter
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0019_alter_renter_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='thai_citizenship_id_card',
            field=models.ImageField(blank=True, null=True, upload_to=renthub.models.renter.upload_to_renter_citizenship_directory),
        ),
    ]
