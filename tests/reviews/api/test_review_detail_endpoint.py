from json import dumps

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from reviews.models import Review
from reviews.api.serializers import ReviewSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
    OrdersTestHelpers,
    ReviewsTestHelpers,
)


class SetUpTestCase(TestCase):

    def create_related_objects(self):
        self.customer = AccountsTestHelpers().create_customer()
        self.vendor = AccountsTestHelpers().create_vendor()
        self.category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=self.category,
        )
        InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10,
        )
        self.order = OrdersTestHelpers().create_order(user=self.customer)
        OrdersTestHelpers().create_order_item(
            order=self.order, product=self.product, quantity=10,
        )
        self.review = ReviewsTestHelpers().create_review(
            order=self.order, user=self.customer, product=self.product,
        )

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})
        return super().setUp()


class TestReviewDetailEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ReviewSerializer(
            Review.objects.get(pk=self.review.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Review.objects.count(), 1)

    def test_patch(self):
        response = self.client.patch(
            self.url,
            data=dumps({'rating': 2}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_review = Review.objects.get(pk=response.data['id'])
        serializer = ReviewSerializer(
            Review.objects.get(pk=self.review.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(db_review.rating, 2)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(Review.objects.count(), 0)
