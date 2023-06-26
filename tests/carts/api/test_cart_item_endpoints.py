from json import dumps

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
        self.client.force_authenticate(user=self.admin)
        self.request = Request(APIRequestFactory().get('/'))

    def create_related_objects(self):
        vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.customer = AccountsTestHelpers().create_customer()
        self.product = ProductsTestHelpers().create_product(
            vendor=vendor, category=category
        )
        InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10
        )
        self.cart = CartTestHelpers().create_cart(user=self.customer)
        self.cart_item = CartTestHelpers().create_cart_item(
            cart=self.cart, product=self.product, quantity=10
        )
        self.admin = AccountsTestHelpers().create_admin()

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.cart_item_list_url = reverse('cart-items')
        self.cart_item_detail_url = reverse(
            'cart-item-detail', kwargs={'pk': self.cart_item.pk}
        )
        return super().setUp()


class TestCartItemListEndpoint(SetUpTestCase):

    def test_get_cart_item_list(self):
        response = self.client.get(self.cart_item_list_url)
        serializer = CartItemSerializer(
            CartItem.objects.all(),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(CartItem.objects.count() > 0)


class TestCartItemDetailEdpoint(SetUpTestCase):

    def test_get_cart_item_details(self):
        response  = self.client.get(self.cart_item_detail_url)
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=self.cart_item.pk),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_cart_item(self):
        response = self.client.patch(self.cart_item_detail_url,
                                     data=dumps({'quantity': 5}),
                                     content_type='application/json')
        serializer = CartItemSerializer(
            CartItem.objects.get(pk=self.cart_item.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_cart_item(self):
        response = self.client.delete(self.cart_item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())
