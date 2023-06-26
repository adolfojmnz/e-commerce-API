from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from carts.models import CartItem
from carts.api.serializers import CartItemSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
    CartTestHelpers,
)


class SetUpTestCase(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def create_related_objects(self):
        vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.customer = AccountsTestHelpers().create_customer()
        self.product = ProductsTestHelpers().create_product(
            vendor=vendor, category=category
        )
        InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10
        )
        self.cart = CartTestHelpers().create_cart(user=self.customer)

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('customer-cart-items')


class TestCartItemListEndpoint(SetUpTestCase):

    def test_get(self):
        CartTestHelpers().create_cart_item(
            cart=self.cart, product=self.product, quantity=10
        )
        response = self.client.get(self.url)
        serializer = CartItemSerializer(
            CartItem.objects.all(),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_post(self):
        data = {
            'product_id': self.product.pk,
            'quantity': 10,
        }
        response = self.client.post(self.url, data)
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(CartItem.objects.count(), 1)
