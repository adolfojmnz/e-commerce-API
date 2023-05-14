from django.test import TestCase

from inventory.models import InventoryItem

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
)


class SetUp(TestCase):

    def create_related_objects(self):
        vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=vendor, category=category
        )

    def setUp(self):
        self.create_related_objects()
        self.inventory_item = InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10
        )
        return super().setUp()


class InventoryModelTests(SetUp):

    def test_inventory_item_created(self):
        self.assertTrue(InventoryItem.objects.all().exists())
        db_inventory_item = InventoryItem.objects.get(pk=self.inventory_item.pk)
        self.assertEqual(db_inventory_item.product, self.product)
        self.assertEqual(db_inventory_item.quantity, 10)

