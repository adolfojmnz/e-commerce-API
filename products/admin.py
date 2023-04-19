from django.contrib import admin

from products.models import Product, Inventory


admin.site.register(Product)
admin.site.register(Inventory)
