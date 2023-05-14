from json import dumps

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.data import (
    customer_single as customer_data,
)
from tests.helpers import AccountsTestHelpers



class SetUpMixin(TestCase):

    def setUp(self):
        self.user = AccountsTestHelpers().create_user()
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client = Client()
        return super().setUp()


class TestUsers(SetUpMixin):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_put(self):
        response = self.client.put(self.url,
                                   data=dumps(customer_data),
                                   content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_patch(self):
        response = self.client.patch(self.url,
                                     data=dumps({'username': 'username'}),
                                     content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_delete(self):
        response = self.client.delete(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(serializer.data, [])
        self.assertEqual(response.data, None)
