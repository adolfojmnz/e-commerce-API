from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from accounts.tests.helpers import UserTestMixin

from categories.tests.helpers import create_category

from products.models import Product
from products.tests.data import product_data
from products.tests.helpers import create_products_list
from products.api.serializers import ProductSerializer


class SetUpTestCase(UserTestMixin, TestCase):

    def setUp(self):
        self.category = create_category()
        self.vendor = self.create_vendor()

        product_data['vendor'] = self.vendor
        product_data['specifications'] = dumps(
            product_data['specifications']
        )
        product_data['category'] = reverse(
            'category-detail',
            kwargs={'pk': self.category.id},
        )

        factory = APIRequestFactory()
        self.request = Request(factory.get('/'))

        self.client = APIClient()
        self.client.force_authenticate(user=self.vendor)


class ProductListEndpointTestCase(SetUpTestCase):

    def test_post(self):
        response = self.client.post(reverse('products'),
                                    data=product_data)
        serializer = ProductSerializer(
            Product.objects.get(pk=response.data['id']),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_get(self):
        create_products_list(self.vendor, self.category)
        response = self.client.get(reverse('products'))
        serializer = ProductSerializer(Product.objects.all(),
                                       many=True,
                                       context={'request': self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Product.objects.count() > 1)
