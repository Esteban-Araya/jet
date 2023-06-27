# Generated by Django 4.1.1 on 2023-06-27 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Devices",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=30, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("device_type", models.CharField(max_length=50)),
                ("turn_on", models.BooleanField(default=False)),
                (
                    "id_user_main",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="my_devices",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "users_id",
                    models.ManyToManyField(
                        null=True, related_name="devices", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
