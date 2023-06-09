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

    def setUp(self):
        self.create_related_objects()
        self.authenticate()


class InventoryItemListEndpointTestCase(SetUpTestCase):

    def test_post(self):
        response = self.client.post(reverse('inventory-items'),
            data={'product': self.product.pk, 'quantity': 10},
        )
        serializer = InventoryItemSerializer(InventoryItem.objects.get(
            pk=response.data['id']),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get().quantity, 10)
        self.assertEqual(InventoryItem.objects.get().product, self.product)

    def test_get(self):
        InventoryTestHelpers().create_inventory_item(product=self.product,
                                                     quantity=10)
        response = self.client.get(reverse('inventory-items'))
        serializer = InventoryItemSerializer(InventoryItem.objects.all(),
                                             many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
