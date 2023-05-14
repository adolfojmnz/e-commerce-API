from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Category
from categories.api.serializers import CategorySerializer

from tests.helpers import CategoriesTestHelpers
from tests.data import category_single as category_data


class SetUpTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('categories')
        return super().setUp()


class InventoryItemListEndppointTestCase(SetUpTestCase):

    def test_get(self):
        CategoriesTestHelpers().create_category()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CategorySerializer(Category.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Category.objects.count(), 1)

    def test_post(self):
        response = self.client.post(self.url, data=category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = CategorySerializer(
            Category.objects.get(pk=response.data['id'])
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Category.objects.count(), 1)
