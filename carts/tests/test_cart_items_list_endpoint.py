from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from carts.models import CartItem
from carts.tests.helpers import create_cart, create_cart_item
from carts.api.serializers import CartItemSerializer


class SetUpTestCase(TestCase):

    def setUp(self):
        self.product = create_product()
        self.customer = UserTestMixin().create_customer()
        self.cart = create_cart(user=self.customer)

        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('cart-items')


class TestCartItemListEndpoint(SetUpTestCase):

    def test_get(self):
        create_cart_item(self.cart, self.product)
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
            'cart': self.cart.id,
            'product': reverse('product-detail', kwargs={'pk': self.product.id}),
            'quantity': 10,
            'sub_total': self.product.price * 10,
        }
        response = self.client.post(self.url, data)
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(CartItem.objects.count(), 1)

