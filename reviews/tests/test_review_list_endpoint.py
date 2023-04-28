from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from accounts.tests.helpers import UserTestMixin

from products.tests.helpers import create_product

from orders.tests.helpers import create_order, create_order_item

from reviews.models import Review
from reviews.api.serializers import ReviewSerializer
from reviews.tests.helpers import create_review
from reviews.tests.data import review_data


class SetUpTestCase(UserTestMixin, TestCase):

    def setUp(self):
        self.customer = self.create_customer()
        self.product = create_product()
        order = create_order(user=self.customer)
        self.order = create_order_item(product=self.product, order=order)

        self.client = APIClient()
        self.client.force_authenticate(user=self.customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('reviews')


class TestReviewListEndpoint(SetUpTestCase):

    def test_get(self):
        create_review(user=self.customer, product=self.product)
        response = self.client.get(self.url)
        serializer = ReviewSerializer(
            Review.objects.all(),
            many=True,
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Review.objects.count(), 1)

    def test_post(self):
        review_data['product'] = self.product.pk
        review_data['user'] = self.customer.pk
        review_data['order'] = self.order.pk

        reponse = self.client.post(self.url, data=review_data)
        created_review = Review.objects.get(pk=reponse.data['id'])
        serializer = ReviewSerializer(created_review,
                                      context={'request': self.request})
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reponse.data, serializer.data)
        self.assertEqual(created_review.title, review_data['title'])
        self.assertEqual(created_review.text, review_data['text'])
        self.assertEqual(created_review.rating, review_data['rating'])
        self.assertEqual(created_review.user, self.customer)
        self.assertEqual(created_review.product, self.product)
