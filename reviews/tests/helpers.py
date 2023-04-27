from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from reviews.models import Review
from reviews.tests.data import review_data


def create_review(user=None, product=None, review_data=review_data):
    return Review.objects.create(
        user = user or UserTestMixin().create_customer(),
        product = product or create_product(),
        **review_data,
    )

