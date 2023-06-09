from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
)


class SetUpTestCase(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.vendor)

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=category
        )
        self.inventory_item = InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse(
            'inventory-item-detail', kwargs={'pk': self.inventory_item.pk}
        )


class InventoryItemDetailEndpointTestCase(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = InventoryItemSerializer(
            InventoryItem.objects.get(pk=response.data['id'])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)

    def test_patch(self):
        response = self.client.patch(self.url, data={'quantity': 5})
        serializer = InventoryItemSerializer(
            InventoryItem.objects.get(pk=self.inventory_item.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(
            InventoryItem.objects.get(pk=self.inventory_item.pk).quantity,
            5
        )

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(InventoryItem.objects.count(), 0)
