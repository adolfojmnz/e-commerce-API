from django.test import TestCase

from reviews.models import Review

from tests.helpers import AccountsTestHelpers
from tests.helpers import CategoriesTestHelpers
from tests.helpers import ProductsTestHelpers
from tests.helpers import OrdersTestHelpers
from tests.helpers import ReviewsTestHelpers

from tests.data import review_single as review_data


class SetUp(TestCase):

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        self.customer = AccountsTestHelpers().create_customer()
        self.category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=self.category
        )
        self.order = OrdersTestHelpers().create_order(user=self.customer)

    def setUp(self):
        self.create_related_objects()
        self.review = ReviewsTestHelpers().create_review(
            order=self.order, product=self.product, user=self.customer
        )
        return super().setUp()


class ReviewModelTests(SetUp):

    def test_review_created(self):
        self.assertTrue(Review.objects.exists())
        db_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(db_review.order, self.order)
        self.assertEqual(db_review.product, self.product)
        self.assertEqual(db_review.user, self.customer)
        self.assertEqual(db_review.image_url, review_data['image_url'])
        self.assertEqual(db_review.title, review_data['title'])
        self.assertEqual(db_review.text, review_data['text'])
        self.assertEqual(db_review.rating, review_data['rating'])
        self.assertEqual(db_review.date, self.review.date)
