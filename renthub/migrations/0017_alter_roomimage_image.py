# Generated by Django 5.1.2 on 2024-11-20 14:30

import renthub.models.room_image
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renthub', '0016_roomimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=renthub.models.room_image.upload_to_room_directory),
        ),
    ]