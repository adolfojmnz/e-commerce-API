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


class TestAdminEndpointsForCarts(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.request = Request(APIRequestFactory().get('/'))

    def setUp(self):
        self.admin = AccountsTestHelpers().create_admin()
        customer = AccountsTestHelpers().create_customer()
        self.cart = CartTestHelpers().create_cart(user=customer)
        self.cart_list_url = reverse('carts')
        self.cart_detail_url = reverse(
            'cart-detail', kwargs={'pk': self.cart.pk}
        )
        self.authenticate()
        return super().setUp()

    def test_get_cart_list(self):
        response = self.client.get(self.cart_list_url)
        serializer = CartSerializer(
            Cart.objects.all(),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Cart.objects.count() > 0)

    def test_get_cart_detail(self):
        response = self.client.get(self.cart_detail_url)
        serializer = CartSerializer(
            Cart.objects.get(pk=self.cart.pk),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class TestCustomerPermissionOnOnlyAdminsEndpointForCarts(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def setUp(self):
        self.customer = AccountsTestHelpers().create_customer()
        self.cart = CartTestHelpers().create_cart(user=self.customer)
        self.cart_list_url = reverse('carts')
        self.cart_detail_url = reverse(
            'cart-detail', kwargs={'pk': self.cart.pk}
        )
        self.authenticate()
        return super().setUp()

    def test_customer_cannot_get_cart_list(self):
        response = self.client.get(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_create_cart(self):
        response = self.client.post(self.cart_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_get_cart_detail(self):
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_update_cart(self):
        response = self.client.put(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
