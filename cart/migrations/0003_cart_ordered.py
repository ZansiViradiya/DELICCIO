# Generated by Django 4.1.4 on 2023-04-04 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="ordered",
            field=models.BooleanField(default=False),
        ),
    ]
