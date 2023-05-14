from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from reviews.models import Review
from reviews.api.serializers import ReviewSerializer

from tests.data import review_single as review_data
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

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)
        self.request = Request(APIRequestFactory().get('/'))

    def prepare_review_data(self):
        self.review_data = review_data.copy()
        self.review_data['product'] = self.product.pk
        self.review_data['order'] = self.order.pk

    def setUp(self):
        self.create_related_objects()
        self.authenticate()
        self.url = reverse('reviews')
        return super().setUp()


class TestReviewListEndpoint(SetUpTestCase):

    def test_get(self):
        ReviewsTestHelpers().create_review(
            order=self.order, user=self.customer, product=self.product,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ReviewSerializer(
            Review.objects.all(),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Review.objects.count(), 1)

    def test_post(self):
        self.prepare_review_data()
        response = self.client.post(self.url, data=self.review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = ReviewSerializer(
            Review.objects.get(pk=response.data['id']),
            context={'request': self.request},
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Review.objects.count(), 1)
