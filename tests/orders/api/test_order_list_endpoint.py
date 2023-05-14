from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from orders.models import Order
from orders.api.serializers import OrderSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
    CartTestHelpers,
    OrdersTestHelpers,
)


class SetUpTestCase(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        self.customer = AccountsTestHelpers().create_customer()
        category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=category
        )
        self.inventory_item = InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10
        )
        self.cart = CartTestHelpers().create_cart(user=self.customer)
        self.cart_item = CartTestHelpers().create_cart_item(
            cart=self.cart, product=self.product, quantity=10
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('orders')
        return super().setUp()


class TestOrderListEndpoint(SetUpTestCase):

    def test_get(self):
        OrdersTestHelpers().create_order(user=self.customer)
        response = self.client.get(f'{self.url}?user=current')
        serializer = OrderSerializer(
            Order.objects.filter(user=self.customer),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Order.objects.count(), 1)

    def test_post(self):
        response = self.client.post(self.url)
        serializer = OrderSerializer(
            Order.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Order.objects.count(), 1)
