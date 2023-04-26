from django.test import TestCase

from inventory.models import InventoryItem

from products.tests.helpers import create_product


class SetUp(TestCase):

    def setUp(self):
        self.inventory_item = create_product().inventory


class TestInventoryItem(SetUp):

    def test_inventory(self):
        self.assertEqual(
            InventoryItem.objects.filter(pk=self.inventory_item.pk).exists(),
            True
        )
        self.assertEqual(
            InventoryItem.objects.get(pk=self.inventory_item.pk).product,
            self.inventory_item.product,
        )
        self.assertEqual(
            InventoryItem.objects.get(pk=self.inventory_item.pk).quantity,
            1,
        )

