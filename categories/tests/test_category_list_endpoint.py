from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Category
from categories.tests.helpers import create_category
from categories.api.serializers import CategorySerializer


class SetUpTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()


class InventoryItemListEndppointTestCase(SetUpTestCase):

    def test_post(self):
        response = self.client.post(reverse('categories'),
            data={
                'name': 'Test Category',
                'description': 'Test Description',
            }
        )
        serializer = CategorySerializer(Category.objects.get(
            pk=response.data['id']),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(serializer.data['name'], 'Test Category')
        self.assertEqual(serializer.data['description'], 'Test Description')

    def test_get(self):
        create_category()
        response = self.client.get(reverse('categories'))
        serializer = CategorySerializer(Category.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Category.objects.count(), 1)
