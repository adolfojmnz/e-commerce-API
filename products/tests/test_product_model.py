from django.test import TestCase

from accounts.models import User

from products.models import Product
from products.tests.utils import create_product


class SetUp(TestCase):

    def setUp(self):
        self.product = create_product()


class TesteProduct(SetUp):

    def test_product(self):
        self.assertEqual(
            Product.objects.filter(pk=self.product.pk).exists(),
            True,
        )
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).name,
            self.product.name,
        )
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).brand,
            self.product.brand,
        )
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).description,
            self.product.description,
        )
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).specifications,
            self.product.specifications,
        )
        self.assertEqual(
            Product.objects.get(pk=self.product.pk).category,
            self.product.category,
        )

