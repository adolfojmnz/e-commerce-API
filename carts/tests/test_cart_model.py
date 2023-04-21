from django.test import TestCase

from carts.models import Cart
from carts.tests.utils import create_cart


class SetUp(TestCase):

    def setUp(self):
        self.cart = create_cart()


class TestCart(SetUp):

    def test_cart(self):
        self.assertEqual(
            Cart.objects.filter(pk=self.cart.pk).exists(),
            True,
        )
        self.assertEqual(
            Cart.objects.get(pk=self.cart.pk).user,
            self.cart.user,
        )
        self.assertEqual(
            Cart.objects.get(pk=self.cart.pk).total,
            self.cart.total,
        )
        self.assertEqual(
            Cart.objects.get(pk=self.cart.pk).updated_on,
            self.cart.updated_on,
        )

