from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from accounts.models import User
from accounts.api.serializers import UserSerializer
from accounts.tests.data import (
    users_data_list, single_user_data
)


class SetUpMixin(TestCase):

    def setUp(self) -> None:
        self.client = Client()


class TestUsers(SetUpMixin):

    def test_post(self):
        response = self.client.post(reverse('users'), data=single_user_data)
        created_user = User.objects.get(username=single_user_data['username'])
        serializer = UserSerializer(created_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])
        self.assertTrue(created_user.cart.all().exists())

    def test_get(self):
        [User.objects.create(**user_data) for user_data in users_data_list]
        response = self.client.get(reverse('users'))
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])
