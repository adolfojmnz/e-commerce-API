from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APIClient

from products.models import Product, DeletedProduct
from products.api.serializers import ProductSerializer

from tests.data import product_list
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
        self.product = ProductsTestHelpers().create_product(
            self.vendor, self.category
        )
        self.inventory = InventoryTestHelpers().create_inventory_item(
            self.product, quantity=10
        )

    def get_serialized_product(self):
        return ProductSerializer(
            Product.objects.get(pk=self.product.pk)
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse(
            'product-detail', kwargs={'pk': self.product.pk}
        )
        return super().setUp()


class ProductDetailEndpointTestCase(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_serialized_product()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_put(self):
        response = self.client.put(
            self.url,
            data=dumps(product_list[0]),
            content_type='application/json',
        )
        serializer = self.get_serialized_product()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_patch(self):
        response = self.client.patch(
            self.url,
            data=dumps({'name': 'New Name'}),
            content_type='application/json',
        )
        serializer = self.get_serialized_product()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            DeletedProduct.objects.filter(product=self.product).exists()
        )
