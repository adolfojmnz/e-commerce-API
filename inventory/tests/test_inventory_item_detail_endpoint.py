from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from products.tests.helpers import create_product

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer



class SetUpTestCase(TestCase):

    def setUp(self):
        self.inventory = create_product().inventory
        self.client = APIClient()


class InventoryItemDetailEndppointTestCase(SetUpTestCase):

    def test_get(self):
        response = self.client.get(
            reverse('inventory-item-detail',
            kwargs={'pk': self.inventory.pk}),
        )
        serializer = InventoryItemSerializer(InventoryItem.objects.get(
            pk=response.data['id']),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(
            InventoryItem.objects.get(pk=self.inventory.pk).quantity,
            1
        )

    def test_patch(self):
        response = self.client.patch(
            reverse('inventory-item-detail',
            kwargs={'pk': self.inventory.pk}),
            data={'quantity': 2},
        )
        serializer = InventoryItemSerializer(InventoryItem.objects.get(
            pk=self.inventory.pk),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(
            InventoryItem.objects.get(pk=self.inventory.pk).quantity,
            2
        )

    def test_delete(self):
        response = self.client.delete(
            reverse('inventory-item-detail',
            kwargs={'pk': self.inventory.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)
