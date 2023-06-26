from json import dumps

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.helpers import AccountsTestHelpers


class TestAdminDetailEndpoint(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.admin = AccountsTestHelpers().create_admin()
        self.client.force_authenticate(user=self.admin)

    def setUp(self) -> None:
        self.authenticate()
        self.url = reverse('admin-detail', kwargs={'pk': self.admin.pk})
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.admin.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_patch(self):
        response = self.client.patch(self.url,
                                     data=dumps({'username': 'username'}),
                                     content_type='application/json')
        serializer = UserSerializer(User.objects.get(pk=self.admin.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_delete(self):
        response = self.client.delete(self.url)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOtherAdminPermissionOnAdminDetailEndpoint(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.admin = AccountsTestHelpers().create_admin()
        self.other_admin = AccountsTestHelpers().create_user(is_admin=True)
        self.client.force_authenticate(user=self.admin)

    def setUp(self) -> None:
        self.authenticate()
        self.url = reverse('admin-detail', kwargs={'pk': self.other_admin.pk})
        return super().setUp()

    def test_admin_can_get_other_admin(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.other_admin.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_admin_can_not_update_other_admin(self):
        response = self.client.patch(self.url,
                                     data=dumps({'username': 'username'}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(
            User.objects.get(pk=self.other_admin.pk).username, 'username'
        )

    def test_admin_can_not_delete_other_admin(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.get(pk=self.other_admin.pk).is_active)


class TestSuperuserPermissionOnAdminDetailEndpoint(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.superuser = AccountsTestHelpers().create_superuser()
        self.client.force_authenticate(user=self.superuser)

    def setUp(self) -> None:
        self.authenticate()
        self.admin = AccountsTestHelpers().create_admin()
        self.url = reverse('admin-detail', kwargs={'pk': self.admin.pk})
        return super().setUp()

    def test_superuser_can_get_admin(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(User.objects.get(pk=self.admin.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_superuser_can_delete_admin(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.admin.pk).is_active, False)

    def test_superuser_can_update_admin(self):
        response = self.client.patch(self.url,
                                     data=dumps({'username': 'username'}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.get(pk=self.admin.pk).username, 'username'
        )
