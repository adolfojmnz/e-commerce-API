# Generated by Django 4.2 on 2023-04-20 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_inventory_quantity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='vendor',
        ),
    ]