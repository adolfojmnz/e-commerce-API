# Generated by Django 4.2.2 on 2023-07-22 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_remove_image_related_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='created_at',
            new_name='added_on',
        ),
    ]
