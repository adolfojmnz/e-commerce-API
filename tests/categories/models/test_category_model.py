from django.test import TestCase

from categories.models import Category

from tests.helpers import CategoriesTestHelpers
from tests.data import category_single as category_data


class SetUp(TestCase):

    def setUp(self):
        categories_helpers = CategoriesTestHelpers()
        self.category = categories_helpers.create_category()
        return super().setUp()


class TestCategory(SetUp):

    def test_category_model(self):
        self.assertEqual(
            Category.objects.filter(pk=self.category.pk).exists(), True
        )
        db_category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(db_category.name, category_data["name"])
        self.assertEqual(db_category.description, category_data["description"])
