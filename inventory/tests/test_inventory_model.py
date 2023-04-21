from django.test import TestCase

from inventory.models import Inventory

from inventory.tests.utils import create_inventory_item


class SetUp(TestCase):

    def setUp(self):
        self.inventory_item = create_inventory_item()


class TestInventory(SetUp):

    def test_inventory(self):
        self.assertEqual(
            Inventory.objects.filter(pk=self.inventory_item.pk).exists(),
            True
        )
        self.assertEqual(
            Inventory.objects.get(pk=self.inventory_item.pk).product,
            self.inventory_item.product,
        )
        self.assertEqual(
            Inventory.objects.get(pk=self.inventory_item.pk).quantity,
            10,
        )

