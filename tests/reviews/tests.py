from django.test import TestCase

from accounts.models import User
from reviews.models import Review

from tests.watches.tests import SetUpMixin as SetUpWatchMixin


class SetUpMixin(SetUpWatchMixin):

    REVIEW_DATA = {
        'title': 'Loving It',
        'text': """Very impressed with this watch and how quickly I received
            this item. The shipping box came damaged and had a slight delay over
            the Thanksgiving (USA) weekend but to no fault of the vendor. The
            item itself was packaged carefully and was protected from any damages
            during shipping, so I appreciate the care and precaution taken by
            them ahead of shipping said item.""",
        'rating': 5,
        'date': '2023-04-11',
    }

    def setUp(self):
        self.user = User.objects.create(username='customer',
                                            password='cust#passwd')
        self.vendor = self.create_vendor()
        self.collection = self.create_collection(self.vendor)
        self.watch = self.create_watch(self.collection)
        self.review = self.create_review(self.watch, self.user)

    def create_review(self, watch, user):
        self.REVIEW_DATA['watch'] = watch
        self.REVIEW_DATA['user'] = user
        review = Review.objects.create(**self.REVIEW_DATA)
        review.save()
        return review


class TestReview(SetUpMixin, TestCase):

    def setUp(self):
        return super().setUp()

    def test_review(self):
        retrieved_review = Review.objects.get(title=self.review.title)
        self.assertEqual(self.review.pk, retrieved_review.pk)
        self.assertEqual(self.review.watch, retrieved_review.watch)
        self.assertEqual(self.review.user, retrieved_review.user)
        self.assertEqual(self.review.title, retrieved_review.title)
        self.assertEqual(self.review.text, retrieved_review.text)
        self.assertEqual(self.review.rating, retrieved_review.rating)
        self.assertEqual(self.review.date, retrieved_review.date)
