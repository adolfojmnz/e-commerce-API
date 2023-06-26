from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from orders.models import OrderItem
from orders.api.serializers import OrderItemSerializer


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
        self.order = OrdersTestHelpers().create_order(user=self.customer)
        OrdersTestHelpers().create_order_item(
            order=self.order, product=self.product, quantity=10
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('order-items')
        return super().setUp()


class TestOrderItemListEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = OrderItemSerializer(
            OrderItem.objects.filter(order__user=self.customer),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(OrderItem.objects.count(), 1)

