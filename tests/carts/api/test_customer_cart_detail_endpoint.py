from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from carts.models import Cart
from carts.api.serializers import CartSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CartTestHelpers,
)


class SetUpTestCase(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def setUp(self):
        self.customer = AccountsTestHelpers().create_customer()
        self.cart = CartTestHelpers().create_cart(user=self.customer)
        self.url = reverse('customer-cart')
        self.authenticate()
        return super().setUp()


class TestCartDetailEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = CartSerializer(Cart.objects.get(pk=self.cart.pk),
                                    context={'request': self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Cart.objects.count(), 1)
