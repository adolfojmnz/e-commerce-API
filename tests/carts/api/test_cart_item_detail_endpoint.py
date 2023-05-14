from json import dumps

from django.utils import timezone
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
            product=self.product, quantity=20
        )
        self.cart = CartTestHelpers().create_cart(user=self.customer)
        self.cart_item = CartTestHelpers().create_cart_item(
            cart=self.cart, product=self.product, quantity=10
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('cart-item-detail', kwargs={'pk': self.cart_item.pk})


class TestCartItemDetailEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=self.cart_item.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_patch(self):
        data = {
            'quantity': 20,
            'updated_on': timezone.now().__str__(),
        }
        response = self.client.patch(self.url,
                                     dumps(data),
                                     content_type='application/json')
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=self.cart_item.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(CartItem.objects.count(), 0)
