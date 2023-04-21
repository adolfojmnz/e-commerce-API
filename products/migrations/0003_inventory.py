# Generated by Django 4.2 on 2023-04-19 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_alter_product_specifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to='products.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('vendor', 'product')},
            },
        ),
    ]