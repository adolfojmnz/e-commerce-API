from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from json import dumps

from accounts.models import User
from accounts.api.serializers import UserSerializer

from .data import single_user_data
from .data import users_data_list


class SetUpMixin(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(**single_user_data)
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client = Client()


class TestUsers(SetUpMixin):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_put(self):
        response = self.client.put(self.url,
                                   data=dumps(users_data_list[0]),
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
