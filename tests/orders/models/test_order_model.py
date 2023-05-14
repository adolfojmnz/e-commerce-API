from django.test import TestCase

from orders.models import Order

from tests.helpers import (
    AccountsTestHelpers,
    OrdersTestHelpers,
)


class SetUp(TestCase):

    def setUp(self):
        self.customer = AccountsTestHelpers().create_customer()
        self.order = OrdersTestHelpers().create_order(user=self.customer)
        return super().setUp()


class OrderModelTests(SetUp):

    def test_order_created(self):
        self.assertTrue(Order.objects.all().exists())
        db_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(db_order.user, self.customer)
        self.assertEqual(db_order.created_on, self.order.created_on)
        self.assertEqual(db_order.updated_on, self.order.updated_on)
