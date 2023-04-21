from accounts.tests.utils import create_customer

from products.tests.utils import create_product

from reviews.models import Review
from reviews.tests.data import single_review_data


def create_review():
    review = Review.objects.create(
        user=create_customer(),
        product=create_product(),
        **single_review_data,
    )
    review.save()
    return review

