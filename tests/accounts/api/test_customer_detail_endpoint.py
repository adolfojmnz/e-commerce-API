from json import dumps

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.data import (
    customer_single as customer_data,
    another_customer_single as another_customer_data,
)
from tests.helpers import AccountsTestHelpers


class TestCustomerDetailEndpoint(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.customer = AccountsTestHelpers().create_user()
        self.client.force_authenticate(user=self.customer)
        self.url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_put(self):
        response = self.client.put(self.url,
                                   data=dumps(customer_data),
                                   content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_patch(self):
        response = self.client.patch(self.url,
                                     data=dumps({'username': 'username'}),
                                     content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_delete(self):
        response = self.client.delete(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCustomerPermissionsOnAnotherCustomer(TestCase):

    def setUp(self):
        self.customer = AccountsTestHelpers().create_user()
        self.another_customer = AccountsTestHelpers().create_user(
            user_data=another_customer_data
        )
        self.client = APIClient()
        self.client.force_authenticate(self.customer)
        self.url = reverse(
            'customer-detail', kwargs={'pk': self.another_customer.pk}
        )
        return super().setUp()

    def test_customer_can_get_another_customer(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(
            pk=self.another_customer.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_customer_cannot_update_another_customer(self):
        response = self.client.put(self.url,
                                   data=dumps({'username': 'username'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_delete_another_customer(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAdminPermissionsOnCustomer(TestCase):

    def setUp(self):
        self.customer = AccountsTestHelpers().create_user()
        self.admin = AccountsTestHelpers().create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        return super().setUp()

    def test_admin_can_get_customer(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_admin_can_update_customer(self):
        response = self.client.patch(self.url,
                                   data=dumps({'username': 'username'}),
                                   content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.customer.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data != [])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['username'], 'username')

    def test_admin_can_delete_customer(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         "The user has been set as inactive.")
        self.assertFalse(User.objects.get(pk=self.customer.pk).is_active)
