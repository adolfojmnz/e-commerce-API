from django.test import TestCase

from orders.models import Order
from orders.tests.utils import create_order


class SetUp(TestCase):

    def setUp(self):
        self.order = create_order()


class TestOrder(SetUp):

    def test_order(self):
        self.assertEqual(
            Order.objects.filter(pk=self.order.pk).exists(),
            True,
        )
        self.assertEqual(
            Order.objects.get(pk=self.order.pk).user,
            self.order.user,
        )
        self.assertEqual(
            Order.objects.get(pk=self.order.pk).created_on,
            self.order.created_on,
        )
        self.assertEqual(
            Order.objects.get(pk=self.order.pk).updated_on,
            self.order.updated_on,
        )

