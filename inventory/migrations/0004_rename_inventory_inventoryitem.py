# Generated by Django 4.2 on 2023-04-22 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_category'),
        ('inventory', '0003_alter_inventory_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Inventory',
            new_name='InventoryItem',
        ),
    ]
