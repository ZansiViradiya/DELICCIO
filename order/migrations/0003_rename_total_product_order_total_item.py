# Generated by Django 4.1.4 on 2023-04-11 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_orderitem_food"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="total_product",
            new_name="total_item",
        ),
    ]