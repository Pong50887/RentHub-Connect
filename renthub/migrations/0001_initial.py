# Generated by Django 5.1.1 on 2024-10-10 14:58

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", models.CharField(max_length=500)),
                ("publish_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Rental",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date rented"
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date checkout"
                    ),
                ),
                ("rental_fee", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("approve", "Approve"),
                            ("reject", "Reject"),
                            ("wait", "Wait"),
                        ],
                        default="wait",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Renter",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("phone_number", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("room_number", models.IntegerField(default=0)),
                ("detail", models.CharField(max_length=200)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("availability", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="RoomType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_name", models.CharField(max_length=100)),
                ("description", models.CharField(blank=True, max_length=100)),
                ("ideal_for", models.CharField(blank=True, max_length=100)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="room_images/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_message", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("approve", "Approve"),
                            ("reject", "Reject"),
                            ("wait", "Wait"),
                        ],
                        default="wait",
                        max_length=10,
                    ),
                ),
                ("date_requested", models.DateTimeField()),
                (
                    "rental",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="renthub.rental"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="rental",
            name="renter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="renthub.renter"
            ),
        ),
        migrations.AddField(
            model_name="rental",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="renthub.room"
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="room_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="renthub.roomtype",
            ),
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "room_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="features",
                        to="renthub.roomtype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("detail", models.CharField(max_length=255)),
                ("date", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("approve", "Approve"),
                            ("reject", "Reject"),
                            ("wait", "Wait"),
                        ],
                        default="wait",
                        max_length=10,
                    ),
                ),
                (
                    "rental",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="renthub.rental"
                    ),
                ),
            ],
        ),
    ]
