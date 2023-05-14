from django.test import TestCase

from carts.models import Cart

from tests.helpers import (
    CartTestHelpers,
    AccountsTestHelpers
)


class SetUp(TestCase):

    def create_related_objects(self):
        self.accounts_helpers = AccountsTestHelpers()
        self.cart_helpers = CartTestHelpers()
        self.customer = self.accounts_helpers.create_customer()

    def setUp(self):
        self.create_related_objects()
        self.cart = self.cart_helpers.create_cart(user=self.customer)
        return super().setUp()


class TestCart(SetUp):

    def test_cart_model(self):
        self.assertEqual(
            Cart.objects.filter(pk=self.cart.pk).exists(), True
        )
        db_cart = Cart.objects.get(pk=self.cart.pk)
        self.assertEqual(db_cart.user, self.customer)
        self.assertEqual(db_cart.updated_on, self.cart.updated_on)
