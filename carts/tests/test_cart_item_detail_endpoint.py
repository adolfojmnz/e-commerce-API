from json import dumps

from django.utils import timezone
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
        self.cart_item = create_cart_item(self.cart, self.product)

        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('cart-item-detail', kwargs={'pk': self.cart_item.id})


class TestCartItemDetailEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_patch(self):
        data = {
            'quantity': 20,
            'sub_total': self.product.price * 20,
            'updated_on': timezone.now().__str__(),
        }
        response = self.client.patch(self.url,
                                     dumps(data),
                                     content_type='application/json')
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
