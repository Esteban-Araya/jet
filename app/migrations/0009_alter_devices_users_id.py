# Generated by Django 4.1.1 on 2023-06-21 23:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_alter_devices_id_user_main_alter_devices_users_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devices",
            name="users_id",
            field=models.ManyToManyField(
                null=True, related_name="devices", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
