from inventory.models import InventoryItem


def create_inventory_item(product=None, quantity=10):
    inventory_item = InventoryItem.objects.create(
        product=product,
        quantity=quantity,
    )
    inventory_item.save()
    return inventory_item

