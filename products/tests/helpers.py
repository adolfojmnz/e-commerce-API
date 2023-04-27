from products.models import Product

from accounts.tests.helpers import UserTestMixin

from inventory.tests.helpers import create_inventory_item

from categories.tests.helpers import create_category

from products.tests.data import (
    product_data, product_data_list
)


def create_product(vendor=None, category=None, data=product_data,
                   append_to_inventory=True):

    data['vendor'] = vendor or UserTestMixin().create_vendor()
    data['category'] = category or create_category()

    product = Product.objects.create(**data)
    if append_to_inventory:
        add_product_to_inventory(product)
    return product

def create_products_list(vendor=None, category=None, data=product_data_list):
    return [
        create_product(vendor, category, product_data) for product_data in data
    ]

def add_product_to_inventory(product, quantity=1):
    return create_inventory_item(product, quantity)

