# Generated by Django 4.1.1 on 2023-05-26 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="numero",
            field=models.CharField(max_length=15),
        ),
    ]
