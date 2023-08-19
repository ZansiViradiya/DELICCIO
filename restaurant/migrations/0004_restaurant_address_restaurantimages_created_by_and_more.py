# Generated by Django 4.1.4 on 2023-03-29 12:46

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_address_zipcode"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("restaurant", "0003_alter_restaurant_holidays"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.address",
            ),
        ),
        migrations.AddField(
            model_name="restaurantimages",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="holidays",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("sunday", "Sunday"),
                        ("monday", "Monday"),
                        ("tuesday", "Tuesday"),
                        ("wednesday", "Wednesday"),
                        ("thursday", "Thursday"),
                        ("friday", "Friday"),
                        ("saturday", "Saturday"),
                    ],
                    max_length=10,
                ),
                max_length=3,
                size=None,
            ),
        ),
    ]
