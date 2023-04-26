from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from reviews.models import Review
from reviews.tests.data import single_review_data


def create_review():
    return Review.objects.create(
        user=UserTestMixin().create_customer(),
        product=create_product(),
        **single_review_data,
    )

