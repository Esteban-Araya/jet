# Generated by Django 4.1.1 on 2023-06-10 00:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_alter_devices_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devices",
            name="id",
            field=models.CharField(
                editable=False,
                max_length=30,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
