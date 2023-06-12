# Generated by Django 4.1.1 on 2023-06-12 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_alter_devices_device_type_alter_devices_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devices",
            name="id_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="userMain",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="devices",
            name="users_id",
            field=models.ManyToManyField(
                related_name="users", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
