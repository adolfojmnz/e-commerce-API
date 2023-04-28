from json import dumps

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
        customer = self.create_customer()
        product = create_product()
        order = create_order(user=customer)
        create_order_item(product=product, order=order)
        self.review = create_review(user=customer, product=product)

        self.client = APIClient()
        self.client.force_authenticate(user=customer)

        self.request = Request(APIRequestFactory().get('/'))

        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def update_review_data(self):
        review_data['title'] = 'New Title'
        review_data['text'] = 'New Text'
        review_data['rating'] = 1


class TestReviewListEndpoint(SetUpTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = ReviewSerializer(
            Review.objects.get(pk=self.review.pk),
            context={'request': self.request},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Review.objects.count(), 1)

    def test_patch(self):
        self.update_review_data()
        response = self.client.patch(self.url,
                                     dumps(review_data),
                                     content_type='application/json')
        updated_review = Review.objects.get(pk=response.data['id'])
        serializer = ReviewSerializer(updated_review,
                                      context={'request': self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(updated_review.title, review_data['title'])
        self.assertEqual(updated_review.text, review_data['text'])
        self.assertEqual(updated_review.rating, review_data['rating'])

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
