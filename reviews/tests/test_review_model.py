from django.test import TestCase

from reviews.models import Review
from reviews.tests.utils import create_review


class SetUp(TestCase):

    def setUp(self):
        self.review = create_review()


class TestReview(SetUp):

    def test_review(self):
        self.assertEqual(
            Review.objects.filter(pk=self.review.pk).exists(),
            True,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).product,
            self.review.product,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).user,
            self.review.user,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).title,
            self.review.title,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).text,
            self.review.text,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).rating,
            self.review.rating,
        )
        self.assertEqual(
            Review.objects.get(pk=self.review.pk).date,
            self.review.date,
        )

