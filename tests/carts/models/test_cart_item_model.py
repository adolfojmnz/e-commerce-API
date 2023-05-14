from django.test import TestCase

from carts.models import CartItem

from tests.helpers import (
    CartTestHelpers,
    ProductsTestHelpers,
    CategoriesTestHelpers,
    AccountsTestHelpers,
)


class SetUp(TestCase):

    def create_related_objects(self):
        self.cart_helpers = CartTestHelpers()
        product_helpers = ProductsTestHelpers()
        accounts_helpers = AccountsTestHelpers()
        category_helpers = CategoriesTestHelpers()

        self.vendor = accounts_helpers.create_vendor()
        self.customer = accounts_helpers.create_customer()
        self.category = category_helpers.create_category()
        self.product = product_helpers.create_product(
            vendor=self.vendor, category=self.category
        )
        self.cart = self.cart_helpers.create_cart(
            user=self.customer
        )

    def setUp(self):
        self.create_related_objects()
        self.cart_item = self.cart_helpers.create_cart_item(
            self.cart, self.product, quantity=10
        )
        return super().setUp()


class TestCartItem(SetUp):

    def test_cart_item(self):
        self.assertEqual(
            CartItem.objects.filter(pk=self.cart_item.pk).exists(),
            True,
        )
        db_cart_item = CartItem.objects.get(pk=self.cart_item.pk)
        self.assertEqual(db_cart_item.quantity, 10)
        self.assertEqual(db_cart_item.cart, self.cart)
        self.assertEqual(db_cart_item.product, self.product)
        self.assertEqual(db_cart_item.cart.user, self.customer)
        self.assertEqual(db_cart_item.added_on, self.cart_item.added_on)
        self.assertEqual(db_cart_item.updated_on, self.cart_item.updated_on)


