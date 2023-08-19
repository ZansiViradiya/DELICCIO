# Generated by Django 4.1.4 on 2023-04-10 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0009_rename_address_restaurant_address_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurantimages",
            name="restaurant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="multi_image",
                to="restaurant.restaurant",
            ),
        ),
    ]