from django.test import TestCase

from orders.models import OrderItem
from orders.tests.utils import create_order_item


class SetUp(TestCase):

    def setUp(self):
        self.order_item = create_order_item()


class TestOrderItem(SetUp):

    def test_order_item(self):
        self.assertEqual(
            OrderItem.objects.filter(pk=self.order_item.pk).exists(),
            True,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).order,
            self.order_item.order,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).product,
            self.order_item.product,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).product_values,
            self.order_item.product_values,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).quantity,
            self.order_item.quantity,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).sub_total,
            self.order_item.sub_total,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).added_on,
            self.order_item.added_on,
        )
        self.assertEqual(
            OrderItem.objects.get(pk=self.order_item.pk).updated_on,
            self.order_item.updated_on,
        )

