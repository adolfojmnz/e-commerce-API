from django.test import TestCase

from products.models import Product

from tests.data import product_single as product_data
from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
)


class SetUp(TestCase):

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        self.category = CategoriesTestHelpers().create_category()

    def setUp(self):
        self.create_related_objects()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=self.category
        )
        return super().setUp()


class ProductModelTests(SetUp):

    def test_product_created(self):
        self.assertTrue(Product.objects.exists())
        db_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(db_product.vendor, self.vendor)
        self.assertEqual(db_product.category, self.category)
        self.assertEqual(db_product.name, product_data['name'])
        self.assertEqual(db_product.brand, product_data['brand'])
        self.assertEqual(db_product.price, product_data['price'])
        self.assertEqual(db_product.image_url, product_data['image_url'])
        self.assertEqual(db_product.description, product_data['description'])
        self.assertEqual(
            db_product.specifications, product_data['specifications']
        )
