from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from orders.tests.helpers import create_order, create_order_item

from reviews.models import Review
from reviews.tests.data import review_data


def create_review(user=None, product=None, review_data=review_data):
    user = user or UserTestMixin().create_customer()
    order = create_order(user=user)
    product = product or create_product()
    create_order_item(product=product, order=order)
    return Review.objects.create(
        user = user,
        order = order,
        product = product,
        **review_data,
    )

