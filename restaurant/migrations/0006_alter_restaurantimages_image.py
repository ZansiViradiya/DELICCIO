# Generated by Django 4.1.4 on 2023-03-31 11:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0005_restaurant_contact_alter_restaurant_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurantimages",
            name="image",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.ImageField(
                    default=None, upload_to="images/rest_images/"
                ),
                size=None,
            ),
        ),
    ]
