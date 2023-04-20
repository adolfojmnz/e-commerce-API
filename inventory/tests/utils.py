from products.tests.utils import create_product

from inventory.models import Inventory


def create_inventory_item():
    product = create_product()
    inventory_item = Inventory.objects.create(
        product=product,
        quantity=10,
    )
    inventory_item.save()
    return inventory_item

