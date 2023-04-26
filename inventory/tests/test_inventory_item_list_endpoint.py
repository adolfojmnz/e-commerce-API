from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from products.tests.helpers import create_product, create_products_list

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer



class SetUpTestCase(TestCase):

    def setUp(self):
        self.product = create_product(append_to_inventory=False)
        self.client = APIClient()


class InventoryItemListEndppointTestCase(SetUpTestCase):

    def test_post(self):
        response = self.client.post(reverse('inventory-items'),
            data={'product': self.product.pk, 'quantity': 1},
        )
        serializer = InventoryItemSerializer(InventoryItem.objects.get(
            pk=response.data['id']),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get().quantity, 1)
        self.assertEqual(InventoryItem.objects.get().product, self.product)
        self.assertEqual(
            InventoryItem.objects.get(pk=self.product.inventory.pk).quantity,
            1
        )

    def test_get(self):
        create_products_list(vendor=self.product.vendor,
                             category=self.product.category)
        response = self.client.get(reverse('inventory-items'))
        serializer = InventoryItemSerializer(InventoryItem.objects.all(),
            many=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 2)
