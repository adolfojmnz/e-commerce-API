from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Category
from categories.tests.helpers import create_category
from categories.api.serializers import CategorySerializer


class SetUpTestCase(TestCase):

    def setUp(self):
        self.category = create_category()
        self.url = reverse('category-detail', kwargs={'pk': self.category.pk})
        self.client = APIClient()


class InventoryItemListEndppointTestCase(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = CategorySerializer(Category.objects.get(
            pk=self.category.pk),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Category.objects.count(), 1)

    def test_patch(self):
        response = self.client.patch(self.url, data={'name': 'New Name'})
        serializer = CategorySerializer(
            Category.objects.get(pk=self.category.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def put(self):
        response = self.client.put(
            self.url,
            data={'name': 'New Name', 'description': 'New Description'},
        )
        serializer = CategorySerializer(
            Category.objects.get(pk=self.category.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

