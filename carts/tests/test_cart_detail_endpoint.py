from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from accounts.tests.helpers import UserTestMixin

from carts.models import Cart
from carts.tests.helpers import create_cart
from carts.api.serializers import CartSerializer


class SetUpTestCase(TestCase):

    def setUp(self):
        self.customer = UserTestMixin().create_customer()

        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.cart = create_cart(user=self.customer)

        self.url = reverse('cart-detail', kwargs={'pk': self.cart.id})


class TestCartDetailEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = CartSerializer(Cart.objects.get(pk=self.cart.id),
                                    context={'request': self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Cart.objects.count(), 1)
