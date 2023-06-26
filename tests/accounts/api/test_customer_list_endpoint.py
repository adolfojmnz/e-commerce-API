from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.helpers import AccountsTestHelpers
from tests.data import user_single as user_data



class SetUpTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('customers')
        return super().setUp()


class TestCustomerListEndpoint(SetUpTestCase):

    def test_post(self):
        response = self.client.post(self.url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db_user = User.objects.get(username=user_data['username'])
        serializer = UserSerializer(db_user)
        self.assertTrue(db_user.cart.all().exists())
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_get(self):
        AccountsTestHelpers().create_user_list()
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])
