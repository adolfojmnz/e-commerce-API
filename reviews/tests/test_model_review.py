from django.test import TestCase

from reviews.models import Review
from reviews.tests.helpers import create_review


class SetUpTestCase(TestCase):

    def setUp(self):
        self.review = create_review()


class TestReview(SetUpTestCase):

    def test_review(self):
        self.assertEqual(
            Review.objects.filter(pk=self.review.pk).exists(),
            True,
        )
        retrived_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(
            retrived_review.product,
            self.review.product,
        )
        self.assertEqual(
            retrived_review.user,
            self.review.user,
        )
        self.assertEqual(
            retrived_review.title,
            self.review.title,
        )
        self.assertEqual(
            retrived_review.text,
            self.review.text,
        )
        self.assertEqual(
            retrived_review.rating,
            self.review.rating,
        )
        self.assertEqual(
            retrived_review.date,
            self.review.date,
        )

