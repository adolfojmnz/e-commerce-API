from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from tests.helpers import AccountsTestHelpers
from tests.data import customer_single as customer_data


class SetUp(TestCase):

    def setUp(self):
        self.customer = AccountsTestHelpers().create_customer()
        self.login_data = {
            'username': customer_data['username'],
            'password': customer_data['password'],
        }
        return super().setUp()

    def get_token_obtain_pair_response(self):
        response = self.client.post(
            reverse('token_obtain_pair'), data=self.login_data
        )
        return response


class TestSimpleJWTEndpoint(SetUp):

    def test_token_obtain_pair(self):
        response = self.get_token_obtain_pair_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        response = self.get_token_obtain_pair_response()
        refresh_token = response.data['refresh']
        response = self.client.post(reverse('token_refresh'),
                                    data={'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
