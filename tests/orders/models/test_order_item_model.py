from django.test import TestCase

from orders.models import OrderItem

from tests.helpers import AccountsTestHelpers
from tests.helpers import CategoriesTestHelpers
from tests.helpers import ProductsTestHelpers
from tests.helpers import OrdersTestHelpers


class SetUp(TestCase):

    def create_related_objects(self):
        vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.customer = AccountsTestHelpers().create_customer()
        self.product = ProductsTestHelpers().create_product(
            vendor=vendor, category=category
        )
        self.order = OrdersTestHelpers().create_order(
            user=self.customer
        )

    def setUp(self):
        self.create_related_objects()
        self.order_item = OrdersTestHelpers().create_order_item(
            order = self.order,
            product=self.product,
            quantity=10,
        )
        self.product_values = OrdersTestHelpers().product_values
        return super().setUp()


class OrderItemModelTests(SetUp):

    def test_order_item_created(self):
        self.assertTrue(OrderItem.objects.exists())
        db_order_item = OrderItem.objects.get(pk=self.order_item.pk)
        self.assertEqual(db_order_item.quantity, 10)
        self.assertEqual(db_order_item.order, self.order)
        self.assertEqual(db_order_item.product, self.product)
        self.assertEqual(db_order_item.sub_total, self.product.price * 10)
        self.assertEqual(db_order_item.product_values, self.product_values)

