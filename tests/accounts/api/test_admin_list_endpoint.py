from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.helpers import AccountsTestHelpers
from tests.data import user_single as user_data



class SetUpTestCase(TestCase):

    def authenticate_admin(self):
        self.client = APIClient()
        admin = AccountsTestHelpers().create_admin()
        self.client.force_authenticate(user=admin)

    def authenticate_customer(self):
        self.client = APIClient()
        customer = AccountsTestHelpers().create_user()
        self.client.force_authenticate(user=customer)

    def authenticate_superuser(self):
        self.client = APIClient()
        superuser = AccountsTestHelpers().create_superuser()
        self.client.force_authenticate(user=superuser)


class TestAdminListEndpoint(SetUpTestCase):

    def setUp(self) -> None:
        self.authenticate_admin()
        self.url = reverse('admins')
        return super().setUp()

    def test_post(self):
        data = user_data.copy()
        data.update({'is_staff': True})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db_user = User.objects.get(username=user_data['username'])
        serializer = UserSerializer(db_user)
        self.assertTrue(response.data != [])
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(serializer.data['is_staff'])

    def test_get(self):
        AccountsTestHelpers().create_user_list(is_admin=True)
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])


class TestCustomerPermissionsOnAdminListEndpoint(SetUpTestCase):

    def setUp(self) -> None:
        self.authenticate_customer()
        self.url = reverse('admins')
        return super().setUp()

    def test_customer_can_not_get_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_can_not_create_admin(self):
        response = self.client.post(self.url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSuperuserPermissionOnAdminListEndpoint(SetUpTestCase):

    def setUp(self):
        self.authenticate_superuser()
        self.url = reverse('admins')
        return super().setUp()

    def test_superuser_can_get_admin(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_superuser_can_create_admin(self):
        data = user_data.copy()
        data.update({'is_staff': True})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db_user = User.objects.get(username=user_data['username'])
        serializer = UserSerializer(db_user)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])
