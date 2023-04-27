from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from accounts.tests.helpers import UserTestMixin

from carts.tests.helpers import create_cart, create_cart_item

from orders.models import OrderItem
from orders.api.serializers import OrderItemSerializer
from orders.tests.helpers import create_order, create_order_item


class SetUpTestCase(TestCase):

    def setUp(self):
        customer = UserTestMixin().create_customer()
        cart = create_cart(user=customer)
        cart_item = create_cart_item(cart, quantity=1)
        self.order = create_order(user=customer)
        self.order_item = create_order_item(cart_item.product,
                                            self.order,
                                            quantity=1)

        self.client = APIClient()
        self.client.force_authenticate(user=customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('order-item-detail',
                           kwargs={'pk': self.order_item.pk})


class TestOrderItemListEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = OrderItemSerializer(
            OrderItem.objects.get(pk=self.order_item.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(OrderItem.objects.count(), 1)

