from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from products.models import Product
from products.api.serializers import ProductSerializer

from tests.data import product_single as product_data
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
        self.request = Request(APIRequestFactory().get('/'))

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        self.category = CategoriesTestHelpers().create_category()

    def prepate_product_data(self):
        self.product_data = product_data.copy()
        self.product_data['specifications'] = dumps(
            self.product_data['specifications']
        )
        self.product_data['category'] = self.category.pk
        self.product_data['quantity'] = 10

    def setUp(self):
        self.create_related_objects()
        self.prepate_product_data()
        self.authenticate()
        self.url = reverse('products')
        return super().setUp()


class ProductListEndpointTestCase(SetUpTestCase):

    def test_post(self):
        response = self.client.post(self.url, data=self.product_data)
        serializer = ProductSerializer(
            Product.objects.get(pk=response.data['id']),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_get(self):
        product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=self.category
        )
        InventoryTestHelpers().create_inventory_item(
            product=product, quantity=10
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProductSerializer(
            Product.objects.all(),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Product.objects.count() >= 1)
