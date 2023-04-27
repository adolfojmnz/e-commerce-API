from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from accounts.tests.helpers import UserTestMixin

from carts.tests.helpers import create_cart, create_cart_item

from orders.models import Order
from orders.api.serializers import OrderSerializer
from orders.tests.helpers import create_order, create_order_item


class SetUpTestCase(TestCase):

    def setUp(self):
        self.customer = UserTestMixin().create_customer()
        cart = create_cart(user=self.customer)
        self.cart_item = create_cart_item(cart, quantity=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('orders')


class TestOrderListEndpoint(SetUpTestCase):

    def test_get(self):
        order = create_order(user=self.customer)
        create_order_item(self.cart_item.product, order, quantity=1)
        response = self.client.get(self.url)
        serializer = OrderSerializer(
            Order.objects.all(),
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
