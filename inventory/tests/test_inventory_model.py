from django.test import TestCase

from inventory.models import InventoryItem

from inventory.tests.utils import create_inventory_item


class SetUp(TestCase):

    def setUp(self):
        self.inventory_item = create_inventory_item()


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
            10,
        )

