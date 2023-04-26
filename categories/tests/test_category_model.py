from django.test import TestCase

from categories.models import Category

from categories.tests.helpers import create_category


class SetUp(TestCase):

    def setUp(self):
        self.category = create_category()


class TestCategory(SetUp):

    def test_category(self):
        self.assertEqual(
            Category.objects.filter(pk=self.category.pk).exists(),
            True,
        )
        self.assertEqual(
            Category.objects.get(pk=self.category.pk).name,
            self.category.name,
        )
        self.assertEqual(
            Category.objects.get(pk=self.category.pk).description,
            self.category.description,
        )

