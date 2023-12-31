# Generated by Django 4.1.4 on 2023-03-29 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_address_zipcode"),
        ("restaurant", "0004_restaurant_address_restaurantimages_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.contact",
            ),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.address",
            ),
        ),
    ]
